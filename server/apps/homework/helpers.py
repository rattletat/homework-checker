import os
import hashlib


def generate_sha1(file):
    sha = hashlib.sha1()
    file.seek(0)
    while True:
        buf = file.read(104857600)
        if not buf:
            break
        sha.update(buf)
    sha1 = sha.hexdigest()
    file.seek(0)
    return sha1


def get_exercise_rsc_path(resource, filename):
    lecture_id = resource.exercise.lesson.lecture.id
    lesson_id = resource.exercise.lesson.id
    exercise_id = resource.exercise.id
    return os.path.join(
        "lectures",
        str(lecture_id),
        "lessons",
        str(lesson_id),
        "exercises",
        str(exercise_id),
        "rsc",
        filename,
    )


def get_submission_path(submission, _=None):
    extension = submission.exercise.programming_language
    return os.path.join(
        "submissions",
        str(submission.user.email),
        str(f"{submission.created}_{submission.id}.{extension}"),
    )


def get_tests_path(exercise, _=None):
    lecture_id = exercise.lesson.lecture.id
    lesson_id = exercise.lesson.id
    extension = exercise.programming_language
    return os.path.join(
        "lectures",
        str(lecture_id),
        "lessons",
        str(lesson_id),
        "exercises",
        str(exercise.id),
        f"tests.{extension}",
    )


def get_runner_path(submission, _=None):
    extension = submission.exercise.programming_language
    return os.path.join("runner", f"{extension}-runner.py")
