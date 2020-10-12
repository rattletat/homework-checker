from django.urls import path

from . import views

app_name = "teaching"

urlpatterns = [
    path(route="", view=views.LectureList.as_view(), name="home"),
    path(
        route="lectures/",
        view=views.LectureList.as_view(),
        name="lecture_list",
    ),
    path(
        route="lectures/<slug:lecture_slug>/",
        view=views.LectureDetail.as_view(),
        name="lecture_detail",
    ),
    path(
        route="lectures/<slug:lecture_slug>/lessons/",
        view=views.LessonList.as_view(),
        name="lesson_list",
    ),
    path(
        route="lectures/<slug:lecture_slug>/lessons/<slug:lesson_slug>/",
        view=views.LessonDetail.as_view(),
        name="lesson_detail",
    ),
]
