import os
import uuid
import itertools
from os.path import basename

import docker
from django.utils.encoding import force_str
from tap.parser import Parser

from .helpers import get_runner_path, get_submission_path, get_tests_path
from .models import ExerciseResource

DOCKER_CONFIG = {
    "py": {"image": "app-test-py", "command": "python /app/runner.py"},
    "r": {"image": "app-test-r", "command": "Rscript /app/runner.r --vanilla"},
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

TIMEOUT_ERROR = (
    "Your program executation took too long! It should not take longer than {} seconds."
)
PARSING_ERROR = "A problem occurred during the result parsing."


def run_tests(submission):
    exercise = submission.exercise
    host_root = os.environ["HOST_ROOT_DIR"]

    submission_path = os.path.join(host_root, "mediafiles", str(submission.file))
    tests_path = os.path.join(host_root, "mediafiles", str(exercise.tests))
    runner_path = os.path.join(host_root, "apps/homework/runner/r-runner.r")

    volumes = {
        runner_path: {
            "bind": "/app/runner." + exercise.programming_language,
            "mode": "ro",
        },
        tests_path: {"bind": "/app/tests." + exercise.programming_language, "mode": "ro"},
        submission_path: {
            "bind": "/app/submission." + exercise.programming_language,
            "mode": "ro",
        },
    }

    resources = ExerciseResource.objects.filter(exercise=submission.exercise)
    for resource in resources:
        resource_path = os.path.join(host_root, str(resource.file))
        volumes[resource_path] = {
            "bind": "/app/" + basename(resource.file.name),
            "mode": "ro",
        }

    separator = str(uuid.uuid4())
    config = DOCKER_CONFIG[exercise.programming_language]
    client = docker.from_env()
    try:
        container = client.containers.run(
            config["image"],
            config["command"] + " " + separator,
            volumes=volumes,
            detach=True,
            **DOCKER_SETUP_OPTIONS,
            **DOCKER_SECURITY_OPTIONS,
        )
        container.wait(timeout=exercise.timeout)
        output = container.logs()
        container.stop()
        container.remove(force=True)
        text = force_str(output).split(separator)[1]
    except Exception as e:
        submission.output = TIMEOUT_ERROR + "\n" + str(e)
    else:
        try:
            submission.score = min(get_score_R(text), exercise.max_score)
            if submission.score < exercise.max_score:
                submission.output = get_first_error_R(text)
        except Exception as e:
            submission.output = PARSING_ERROR + "\n" + str(e)
        else:
            submission.full_clean()
            submission.save()
    finally:
        client.containers.prune()


def get_score_R(text):
    parser = Parser()
    gen = parser.parse_text(text)
    return sum(test.ok for test in gen if test.category == "test")


def get_first_error_R(text):
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
