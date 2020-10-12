from rest_framework.routers import DefaultRouter

from .views import LectureReadOnlyModelViewSet, LessonReadOnlyModelViewSet

app_name = "api"

router = DefaultRouter()
router.register("lectures", LectureReadOnlyModelViewSet)
router.register("lessons", LessonReadOnlyModelViewSet)
urlpatterns = router.urls
