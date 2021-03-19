import os
import uuid
from os.path import basename
from django.conf import settings

import docker
from django.utils.encoding import force_str
import tarfile
import tempfile

from tap.parser import Parser

from .models import ExerciseResource

DOCKER_CONFIG = {
    "py": {"image": "rattletat/app-test-py", "command": "python /app/runner.py"},
    "r": {
        "image": "rattletat/app-test-r",
        "command": "Rscript /app/runner.r --vanilla",
    },
}
DOCKER_SETUP_OPTIONS = {
    "working_dir": "/app/",
}
DOCKER_SECURITY_OPTIONS = {
    "user": "1000:1000",
    "network_disabled": True,
    "network_mode": "none",
    "mem_limit": "1g",
    "cap_drop": ["ALL"],
    "privileged": False,
}

PARSING_ERROR = "A problem occurred during the result parsing."


def run_tests(submission):
    exercise = submission.exercise
    extension = exercise.programming_language

    separator = str(uuid.uuid4())
    config = DOCKER_CONFIG[extension]
    client = docker.from_env(timeout=exercise.timeout)
    try:
        container = client.containers.run(
            config["image"],
            command=f"sleep {exercise.timeout}",
            detach=True,
            **DOCKER_SETUP_OPTIONS,
            **DOCKER_SECURITY_OPTIONS,
        )
        for (name, path) in get_file_tuples(submission):
            with tempfile.NamedTemporaryFile() as tmp_file:
                with tarfile.open(fileobj=tmp_file, mode="w") as tar_file:
                    tar_file.add(path, recursive=False, arcname=name)
                    tmp_file.seek(0)
                    container.put_archive("/app/", tmp_file)
        (_, output) = container.exec_run(config["command"] + " " + separator)
        container.stop()
        container.remove(force=True)
        text = force_str(output).split(separator)[1]
    except Exception as e:
        submission.output = str(e)
    else:
        try:
            submission.score = min(get_score(text), exercise.max_score)
            if submission.score < exercise.max_score:
                submission.output = get_first_error(text)
            else:
                submission.output = (
                    "You've reached the maximum number of points. Congratulation!"
                )

        except Exception as e:
            submission.output = PARSING_ERROR + "\n" + str(e)
    finally:
        submission.save()
        client.containers.prune()


def get_file_tuples(submission):
    resources = ExerciseResource.objects.filter(exercise=submission.exercise)
    extension = submission.exercise.programming_language
    submission_tuple = ("submission.py", submission.file.path)
    exercise_tuple = ("tests.py", submission.exercise.tests.path)
    runner_tuple = (
        "runner.py",
        settings.APPS_DIR / os.path.join("homework", "runner", f"runner.{extension}"),
    )
    resource_tuples = [
        (os.path.join("resources", basename(resource.file.name)), resource.file.path)
        for resource in resources
    ]
    return [submission_tuple, exercise_tuple, runner_tuple, *resource_tuples]


def get_score(text):
    parser = Parser()
    lines = text.split("\n")
    gen = parser.parse_text(text)
    return sum(
        test.ok
        for ix, test in enumerate(gen)
        if test.category == "test" and "WARNING" not in lines[ix]
    )


def get_first_error(text):
    try:
        parser = Parser()
        tap_lines = parser.parse_text(text)

        # TODO: refactor
        lines = text.split("\n")
        output = []
        seeking = False
        for ix, tap_line in enumerate(tap_lines):
            if seeking and (tap_line.category == "test" or "Backtrace:" in lines[ix]):
                break
            if not seeking and tap_line.category == "test" and not tap_line.ok:
                seeking = True
            if seeking:
                output.append(lines[ix])

        return "\n".join(output)
    except Exception as e:
        return "No output generated. " + str(e)
