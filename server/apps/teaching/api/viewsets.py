from ..models import Lecture, Lesson
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from sendfile import sendfile


from .serializers import (
    LectureDetailSerializer,
    LectureListSerializer,
    LessonDetailSerializer,
    LessonListSerializer,
)


class LectureReadOnlyModelViewSet(ReadOnlyModelViewSet):
    queryset = Lecture.objects.all()
    lookup_field = "slug"
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return LectureDetailSerializer
        elif self.action == "list":
            return LectureListSerializer
