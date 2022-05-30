from django.urls import path

from apps.teaching.api import views as teaching_views
from apps.homework.api import views as homework_views
from apps.accounts.api import views as account_views
from apps.flatpages.api import views as flatpages_views
from rest_framework_simplejwt.views import TokenRefreshView

app_name = "api"

urlpatterns = [
    path("lectures/", teaching_views.EnrolledLectureListView.as_view()),
    path(
        "lectures/register/<slug:registration_code>",
        view=teaching_views.LectureRegister.as_view(),
    ),
    path(
        "lectures/<slug:slug>/",
        view=teaching_views.LectureRetrieveView.as_view(),
    ),
    path(
        "lectures/<slug:lecture_slug>/resources/<slug:resource_id>",
        view=teaching_views.LectureResourceDownload.as_view(),
        name="lecture_download",
    ),
    path(
        "lectures/<slug:lecture_slug>/lessons/<slug:lesson_slug>/",
        view=teaching_views.LessonRetrieveView.as_view(),
    ),
    path(
        "lectures/<slug:lecture_slug>/lessons/<slug:lesson_slug>/exercises/",
        view=homework_views.ExerciseListView.as_view(),
    ),
    path(
        "lectures/<slug:lecture_slug>/lessons/<slug:lesson_slug>/exercises/status",
        view=teaching_views.LessonScoreStatusView.as_view(),
    ),
    path(
        "lectures/<slug:lecture_slug>/lessons/<slug:lesson_slug>/resources/<slug:resource_id>",
        view=teaching_views.LessonResourceDownload.as_view(),
        name="lesson_download",
    ),
    path(
        "exercises/<slug:exercise_id>/submissions/<slug:submission_id>",
        view=homework_views.SubmissionDownload.as_view(),
        name="submission_download",
    ),
    path(
        "exercises/<slug:exercise_id>/submissions/",
        view=homework_views.SubmissionListView.as_view(),
    ),
    path(
        "exercises/<slug:exercise_id>/submit",
        view=homework_views.ExerciseSubmitView.as_view(),
    ),
    path("accounts/signup", account_views.SignUpView.as_view(), name="signup"),
    path("accounts/login", account_views.LogInView.as_view(), name="login"),
    path("accounts/profile/", account_views.ProfileView.as_view()),
    path(
        "flatpages/<slug:page_slug>/",
        view=flatpages_views.PageView.as_view(),
    ),
    path("token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
]
