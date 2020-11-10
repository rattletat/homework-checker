from datetime import timedelta
from django.utils.timezone import now

import pytest
from django.db import IntegrityError
from django.core.exceptions import ValidationError

from apps.homework.models import Exercise
from tests.teaching.factories import LessonFactory

from .factories import ExerciseFactory, SubmissionFactory

YESTERDAY = now() - timedelta(days=1)
TOMORROW = now() + timedelta(days=1)


@pytest.mark.django_db
class TestExercise:
    def test_string_repr_contains_exercise_lesson_and_exercise_title(self):
        exercise = ExerciseFactory(title="Simple Math Problem")
        assert exercise.lesson.lecture.title in str(exercise)
        assert exercise.lesson.title in str(exercise)
        assert exercise.title in str(exercise)

    def test_unique_title_per_lesson_invariant(self):
        exercise = ExerciseFactory(title="The Riemann Hypothesis")

        with pytest.raises(IntegrityError):
            ExerciseFactory(title="The Riemann Hypothesis", lesson=exercise.lesson)

    def test_automatic_slug_creation(self):
        ExerciseFactory(title="The Unknotting Problem")
        exercise = Exercise.objects.last()

        assert exercise.slug == "the-unknotting-problem"


@pytest.mark.django_db
class TestSubmission:
    def test_submissions_only_before_lecture_end_validation(self):
        lesson = LessonFactory(end=YESTERDAY)
        exercise = ExerciseFactory(lesson=lesson)
        submission = SubmissionFactory(exercise=exercise)

        with pytest.raises(ValidationError):
            submission.full_clean()

    def test_submissions_only_after_lecture_start_validation(self):
        lesson = LessonFactory(start=TOMORROW)
        exercise = ExerciseFactory(lesson=lesson)
        submission = SubmissionFactory(exercise=exercise)

        with pytest.raises(ValidationError):
            submission.full_clean()
