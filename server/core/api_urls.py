from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.teaching.api import viewsets as teaching_viewsets
from apps.teaching.api import views as teaching_views
from apps.homework.api import views as homework_views
from apps.accounts.api import views as account_views
from rest_framework_simplejwt.views import TokenRefreshView

app_name = "api"

router = DefaultRouter()
# Problem -> not unique lessons
router.register("lectures", teaching_viewsets.LectureReadOnlyModelViewSet)

urlpatterns = router.urls
urlpatterns += [
    path(
        "lectures/<slug:lecture_slug>/signup",
        view=teaching_views.LectureSignUp.as_view(),
    ),
    path(
        "lectures/<slug:lecture_slug>/status",
        view=teaching_views.LectureStatus.as_view(),
    ),
    path(
        "lectures/<slug:lecture_slug>/resources/<slug:resource_id>",
        view=teaching_views.LectureResourceDownload.as_view(),
        name="lecture_download",
    ),
    path(
        "lectures/<slug:lecture_slug>/lessons/<slug:lesson_slug>",
        view=teaching_views.LessonRetrieveView.as_view(),
    ),
    path(
        "lectures/<slug:lecture_slug>/lessons/<slug:lesson_slug>/exercises/",
        view=homework_views.ExerciseListView.as_view(),
    ),
    path(
        "lectures/<slug:lecture_slug>/lessons/<slug:lesson_slug>/exercises/status",
        view=homework_views.ExercisesStatus.as_view(),
    ),
    path(
        "lectures/<slug:lecture_slug>/lessons/<slug:lesson_slug>/resources/<slug:resource_id>",
        view=teaching_views.LessonResourceDownload.as_view(),
        name="lesson_download",
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
    path("accounts/profile", account_views.ProfileView.as_view()),
    path("accounts/dashboard", account_views.DashboardView.as_view()),

    path("token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
]
