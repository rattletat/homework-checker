from django.db import IntegrityError
from django.urls import reverse

import pytest
from apps.teaching.models import Lecture, Lesson

from .factories import LectureFactory, LessonFactory


class TestLecture:
    @pytest.mark.django_db
    def test_lecture_factory(self):
        LectureFactory(title="Test Lecture")
        assert Lecture.objects.count() == 1
        assert Lecture.objects.first().title == "Test Lecture"

    @pytest.mark.django_db
    def test_get_absolute_url(self):
        lecture = LectureFactory()
        kwargs = {"lecture_slug": lecture.slug}
        absolute_url = reverse("teaching:lecture_detail", kwargs=kwargs)

        assert lecture.get_absolute_url() == absolute_url

    @pytest.mark.django_db
    def test_string_repr_equals_title(self):
        lecture = LectureFactory(title="Bird Biology")
        assert str(lecture) == lecture.title

    @pytest.mark.django_db
    def test_unique_title_invariant(self):
        LectureFactory(title="The Missing Semester")

        with pytest.raises(IntegrityError):
            LectureFactory(title="The Missing Semester")

    @pytest.mark.django_db
    def test_automatic_slug_creation(self):
        LectureFactory(title="The Missing Semester")
        lecture = Lecture.objects.first()

        assert lecture.slug == "the-missing-semester"


class TestLesson:
    @pytest.mark.django_db
    def test_lesson_factory(self):
        LessonFactory(title="Test Lesson")
        assert Lesson.objects.count() == 1
        assert Lesson.objects.first().title == "Test Lesson"

    @pytest.mark.django_db
    def test_get_absolute_url(self):
        lesson = LessonFactory()
        kwargs = {"lecture_slug": lesson.lecture.slug, "lesson_slug": lesson.slug}
        absolute_url = reverse("teaching:lesson_detail", kwargs=kwargs)

        assert lesson.get_absolute_url() == absolute_url

    @pytest.mark.django_db
    def test_string_repr_contains_both_lecture_and_lesson_title(self):
        lesson = LessonFactory(title="Week 99")
        assert lesson.title in str(lesson)
        assert lesson.lecture.title in str(lesson)

    @pytest.mark.django_db
    def test_unique_title_per_lecture_invariant(self):
        lesson = LessonFactory(title="Lesson 1")

        with pytest.raises(IntegrityError):
            LessonFactory(title="Lesson 1", lecture=lesson.lecture)

    @pytest.mark.django_db
    def test_duplicate_titles_for_different_lectures(self):
        lecture_1 = LectureFactory(title="Lecture 1")
        lecture_2 = LectureFactory(title="Lecture 2")
        LessonFactory(title="Lesson 1", lecture=lecture_1)
        LessonFactory(title="Lesson 1", lecture=lecture_2)

        assert Lesson.objects.count() == 2

    # @pytest.mark.django_db
    # def test_test(self):
    #     lecture_1 = LectureFactory()
    #     lecture_2 = LectureFactory()
    #     assert lecture_1 == lecture_2
