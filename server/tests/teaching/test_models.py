from datetime import timedelta

import pytest
from apps.teaching.models import Lecture, Lesson
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.urls import reverse
from django.utils.timezone import now

from .factories import LectureFactory, LessonFactory

YESTERDAY = now() - timedelta(days=1)
TOMORROW = now() + timedelta(days=1)


@pytest.mark.django_db
class TestLecture:
    def test_lecture_factory(self):
        LectureFactory(title="Test Lecture")
        assert Lecture.objects.count() == 1
        assert Lecture.objects.first().title == "Test Lecture"

    def test_string_repr_contains_title(self):
        lecture = LectureFactory(title="Bird Biology")
        assert lecture.title in str(lecture)

    def test_unique_title_invariant(self):
        LectureFactory(title="The Missing Semester")

        with pytest.raises(IntegrityError):
            LectureFactory(title="The Missing Semester")

    def test_automatic_slug_creation(self):
        LectureFactory(title="The Missing Semester")
        lecture = Lecture.objects.first()

        assert lecture.slug == "the-missing-semester"

    def test_start_date_before_end_date_validation(self):
        lecture = LectureFactory(start=TOMORROW, end=YESTERDAY)
        with pytest.raises(ValidationError):
            lecture.full_clean()


@pytest.mark.django_db
class TestLesson:
    def test_string_repr_contains_both_lecture_and_lesson_title(self):
        lesson = LessonFactory(title="Week 99")
        assert lesson.title in str(lesson)
        assert lesson.lecture.title in str(lesson)

    def test_unique_title_per_lecture_invariant(self):
        lesson = LessonFactory(title="Lesson 1")

        with pytest.raises(IntegrityError):
            LessonFactory(title="Lesson 1", lecture=lesson.lecture)

    def test_duplicate_titles_for_different_lectures_allowed(self):
        lecture_1 = LectureFactory(title="Lecture 1")
        lecture_2 = LectureFactory(title="Lecture 2")
        LessonFactory(title="Lesson 1", lecture=lecture_1)
        LessonFactory(title="Lesson 1", lecture=lecture_2)

        assert Lesson.objects.count() == 2

    def test_start_date_before_end_date_validation(self):
        lesson = LessonFactory(start=TOMORROW, end=YESTERDAY)
        with pytest.raises(ValidationError):
            lesson.full_clean()

    def test_lesson_period_not_before_lecture_starts_validation(self):
        lecture = LectureFactory(start=now())
        lesson1 = LessonFactory(lecture=lecture, start=YESTERDAY)
        lesson2 = LessonFactory(lecture=lecture, end=YESTERDAY)

        with pytest.raises(ValidationError):
            lesson1.full_clean()
        with pytest.raises(ValidationError):
            lesson2.full_clean()

    def test_lesson_period_not_after_lecture_ends_validation(self):
        lecture = LectureFactory(end=now())
        lesson1 = LessonFactory(lecture=lecture, start=TOMORROW)
        lesson2 = LessonFactory(lecture=lecture, end=TOMORROW)

        with pytest.raises(ValidationError):
            lesson1.full_clean()
        with pytest.raises(ValidationError):
            lesson2.full_clean()
