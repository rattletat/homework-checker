from apps.teaching.models import Lecture, Lesson
from rest_framework.viewsets import ReadOnlyModelViewSet

from .serializers import (LectureDetailSerializer, LectureSerializer,
                          LessonSerializer)


class LectureReadOnlyModelViewSet(ReadOnlyModelViewSet):
    queryset = Lecture.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return LectureDetailSerializer
        else:
            return LectureSerializer


class LessonReadOnlyModelViewSet(ReadOnlyModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
