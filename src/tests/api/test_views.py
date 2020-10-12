import pytest
from tests.teaching.factories import LectureFactory, LessonFactory


class TestLectureAPI:
    @pytest.mark.django_db
    def test_get_single_lecture(self, client):
        lecture = LectureFactory()
        response = client.get(f"/api/lectures/{lecture.id}/")
        assert response.status_code == 200
        assert response.data["title"] == lecture.title

    @pytest.mark.django_db
    def test_get_single_lecture_incorrect_id(self, client):
        response = client.get("/api/lectures/foo/")
        assert response.status_code == 404

    @pytest.mark.django_db
    def test_get_all_lectures(self, client):
        lecture_1 = LectureFactory(title="Introduction to Thermodynamics")
        lecture_2 = LectureFactory(title="Introduction to Coffee Brewing")
        response = client.get("/api/lectures/")
        assert response.status_code == 200
        assert len(response.data) == 2
        assert response.data[0]["title"] == lecture_1.title
        assert response.data[1]["title"] == lecture_2.title


class TestLessonAPI:
    @pytest.mark.django_db
    def test_get_single_lesson(self, client):
        lesson = LessonFactory()
        response = client.get(f"/api/lessons/{lesson.id}/")
        assert response.status_code == 200
        assert response.data["title"] == lesson.title

    @pytest.mark.django_db
    def test_get_single_lesson_incorrect_id(self, client):
        response = client.get("/api/lessons/foo/")
        assert response.status_code == 404

    @pytest.mark.django_db
    def test_get_all_lessons(self, client):
        lesson_1 = LessonFactory(title="Lesson 1")
        lesson_2 = LessonFactory(title="Lesson 2")
        response = client.get("/api/lessons/")
        assert response.status_code == 200
        assert len(response.data) == 2
        assert response.data[0]["title"] == lesson_1.title
        assert response.data[1]["title"] == lesson_2.title
