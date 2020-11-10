from apps.teaching.models import Lecture, Lesson, LectureResource, LessonResource
from django.contrib.auth.decorators import login_required
from rest_framework.viewsets import ReadOnlyModelViewSet, GenericViewSet
from rest_framework.mixins import RetrieveModelMixin
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

    def get_serializer_class(self):
        if self.action == "retrieve":
            return LectureDetailSerializer
        elif self.action == "list":
            return LectureListSerializer


class LessonReadOnlyModelViewSet(ReadOnlyModelViewSet):
    queryset = Lesson.objects.all()
    lookup_field = "slug"

    def get_serializer_class(self):
        if self.action == "retrieve":
            return LessonDetailSerializer
        else:
            return LessonListSerializer


# @login_required
# def download_public_file(request, uuid):
#     resource = LectureResource.objects.get(id=uuid)
#     return sendfile(request, resource.file.path, attachment=True)
