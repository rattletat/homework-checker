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
    lecture_slug = resource.exercise.lesson.lecture.slug
    lesson_slug = resource.exercise.lesson.slug
    exercise_slug = resource.exercise.slug
    return os.path.join(
        "lectures",
        str(lecture_slug),
        "lessons",
        str(lesson_slug),
        "exercises",
        str(exercise_slug),
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
    lecture_slug = exercise.lesson.lecture.slug
    lesson_slug = exercise.lesson.slug
    extension = exercise.programming_language
    return os.path.join(
        "lectures",
        str(lecture_slug),
        "lessons",
        str(lesson_slug),
        "exercises",
        str(exercise.slug),
        f"tests.{extension}",
    )


def get_runner_path(submission, _=None):
    extension = submission.exercise.programming_language
    return os.path.join("runner", f"{extension}-runner.py")
