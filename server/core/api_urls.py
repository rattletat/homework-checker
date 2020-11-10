from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.teaching.api import viewsets as teaching_viewsets
from apps.teaching.api import views as teaching_views
from apps.homework.api import viewsets as homework_views
from apps.accounts.api import views as account_views
from rest_framework_simplejwt.views import TokenRefreshView

app_name = "api"

router = DefaultRouter()
router.register("lectures", teaching_viewsets.LectureReadOnlyModelViewSet)
router.register("lessons", teaching_viewsets.LessonReadOnlyModelViewSet)
router.register("exercises", homework_views.ExerciseReadOnlyModelViewSet)
router.register("submissions", homework_views.SubmissionReadOnlyModelViewSet)

urlpatterns = router.urls
urlpatterns += [
    path(
        "lectures/<slug:slug>/signup",
        view=teaching_views.LectureSignUp.as_view(),
        name="lecture_signup",
    ),
    path(
        "lectures/<slug:slug>/status",
        view=teaching_views.LectureStatus.as_view(),
        name="lecture_status",
    ),
    path("accounts/signup", account_views.SignUpView.as_view(), name="signup"),
    path("accounts/login", account_views.LogInView.as_view(), name="login"),
    path("accounts/status", account_views.StatusView.as_view(), name="status"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
