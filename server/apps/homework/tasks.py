import os
import uuid
from os.path import basename

from podman import PodmanClient
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
PODMAN_URI = "/var/run/podman.sock"
RUNTIME_ERROR = "A problem occurred. Please check your program for syntax errors and runtime problems.\n"
PARSING_ERROR = "A problem occurred during the result parsing."


def run_tests(submission):
    exercise = submission.exercise
    extension = exercise.programming_language

    separator = str(uuid.uuid4())
    config = DOCKER_CONFIG[extension]
    try:
        with PodmanClient() as client:
            output = client.containers.run(
                image=config["image"],
                mounts=[
                    {"type": "bind", "source": src, "target": tgt}
                    for (src, tgt) in get_file_tuples(submission)
                ],
                **DOCKER_SETUP_OPTIONS,
                **DOCKER_SECURITY_OPTIONS,
            )
            text = force_str(output).split(separator)[1]
    except Exception as e:
        submission.output = RUNTIME_ERROR + "\n" + str(e)
        print(e)
    else:
        try:
            submission.output = get_first_error(text)
            submission.score = min(
                round(get_score(text) * exercise.multiplier), exercise.max_score
            )
        except Exception as e:
            submission.output = PARSING_ERROR + "\n" + str(e)
    finally:
        submission.save()


def get_file_tuples(submission):
    resources = ExerciseResource.objects.filter(exercise=submission.exercise)
    extension = submission.exercise.programming_language
    submission_tuple = (f"submission.{extension}", submission.file.path)
    exercise_tuple = (f"tests.{extension}", submission.exercise.tests.path)
    resource_tuples = [
        (os.path.join("resources", basename(resource.file.name)), resource.file.path)
        for resource in resources
    ]
    return [submission_tuple, exercise_tuple, *resource_tuples]


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

        if message := "\n".join(output):
            return message
        else:
            return "No output generated."
    except Exception as e:
        return "Exception while parsing traceback: " + str(e)
