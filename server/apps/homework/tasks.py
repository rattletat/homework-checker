import uuid
import docker
from tap.parser import Parser
from os.path import basename

from django.conf import settings
from django.utils.encoding import force_str

from .helpers import get_runner_path, get_submission_path, get_tests_path
from .models import ExerciseResource

DOCKER_CONFIG = {
    "py": {"image": "app-test-py", "command": "python runner.py"},
    "r": {"image": "app-test-r", "command": "R runner.r"},
}
DOCKER_SETUP_OPTIONS = {
    "working_dir": "/app",
}
DOCKER_SECURITY_OPTIONS = {
    "user": "1000:1000",
    "read_only": True,
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

    submission_path = settings.MEDIA_ROOT + get_submission_path(submission, None)
    runner_path = settings.MEDIA_ROOT + get_runner_path(submission, None)
    tests_path = settings.MEDIA_ROOT + get_tests_path(exercise)

    volumes = {
        runner_path: {"bind": "/app/runner.py", "mode": "ro"},
        tests_path: {"bind": "/app/tests.py", "mode": "ro"},
        submission_path: {"bind": "/app/submission.py", "mode": "ro"},
    }

    resources = ExerciseResource.objects.filter(exercise=submission.exercise)
    for resource in resources:
        resource_path = settings.MEDIA_ROOT + resource.file.url
        volumes[resource_path] = {
            "bind": "/app/" + basename(resource.file.name),
            "mode": "ro",
        }

    separator = str(uuid.uuid4())
    client = docker.from_env()
    config = DOCKER_CONFIG[exercise.programming_language]
    try:
        container = client.containers.run(
            config["image"],
            config["command"] + " " + separator,
            **DOCKER_SETUP_OPTIONS,
            **DOCKER_SECURITY_OPTIONS,
            volumes=volumes,
            detach=True,
        )
        container.wait(timeout=exercise.timeout)
        output = container.logs()
        results = force_str(output).split(separator)
        container.remove(force=True)
    except Exception as e:
        submission.output = TIMEOUT_ERROR + "\n" + str(e)
    else:
        try:
            tap_output = results[1]
            submission.score = get_score(tap_output)
            submission.output = get_first_error(tap_output)
        except Exception as e:
            submission.output = PARSING_ERROR + "\n" + str(e)
        else:
            if submission.is_valid():
                submission.save()
            else:
                print("Submission not valid!")


def get_score(tap_output):
    parser = Parser()
    gen = parser.parse_text(tap_output)
    return sum(test.ok for test in gen if test.category == "test")


def get_first_error(tap_output):
    parser = Parser()
    gen = parser.parse_text(tap_output)
    index_gen = (i for i, v in enumerate(gen) if v.category == "test")
    try:
        index = next(index_gen)
        return "\n".join(tap_output.split("\n")[1:index])
    except StopIteration:
        return tap_output
