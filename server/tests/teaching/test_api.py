import pytest
from tests.teaching.factories import LectureFactory, LessonFactory


class TestLectureAPI:
    @pytest.mark.django_db
    def test_get_single_lecture(self, authclient):
        lecture = LectureFactory()
        response = authclient.get(f"/api/lectures/{lecture.slug}/")
        assert response.status_code == 200
        assert response.data["title"] == lecture.title

    @pytest.mark.django_db
    def test_get_single_lecture_incorrect_id(self, authclient):
        response = authclient.get("/api/lectures/foo/")
        assert response.status_code == 404

    @pytest.mark.django_db
    def test_get_all_lectures(self, authclient):
        lecture_1 = LectureFactory(title="Introduction to Thermodynamics")
        lecture_2 = LectureFactory(title="Introduction to Coffee Brewing")
        response = authclient.get("/api/lectures/")
        assert response.status_code == 200
        assert len(response.data) == 2
        assert response.data[0]["title"] == lecture_1.title
        assert response.data[1]["title"] == lecture_2.title


class TestLessonAPI:
    @pytest.mark.django_db
    def test_get_single_lesson(self, authclient):
        lesson = LessonFactory()
        response = authclient.get(f"/api/lessons/{lesson.slug}/")
        assert response.status_code == 200
        assert response.data["title"] == lesson.title

    @pytest.mark.django_db
    def test_get_single_lesson_incorrect_slug(self, authclient):
        response = authclient.get("/api/lessons/foo/")
        assert response.status_code == 404

    @pytest.mark.django_db
    def test_get_all_lessons(self, authclient):
        lesson_1 = LessonFactory(title="Lesson 1")
        lesson_2 = LessonFactory(title="Lesson 2")
        response = authclient.get("/api/lessons/")
        assert response.status_code == 200
        assert len(response.data) == 2
        assert response.data[0]["title"] == lesson_1.title
        assert response.data[1]["title"] == lesson_2.title
