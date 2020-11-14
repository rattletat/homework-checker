from rest_framework import status, response, permissions
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView, ListAPIView
from ..models import Lecture, Lesson, LectureResource, LessonResource
from apps.homework.models import Exercise
from sendfile import sendfile
from .serializers import (
    LessonDetailSerializer,
)


class LectureSignUp(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        lecture = Lecture.objects.get(slug=kwargs["lecture_slug"])
        lecture.participants.add(request.user)
        lecture.save()
        return response.Response({}, status=status.HTTP_200_OK)


class LectureStatus(APIView):
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "lecture_slug"

    def get(self, request, *args, **kwargs):
        lecture = Lecture.objects.get(slug=kwargs["lecture_slug"])
        data = {"registered": request.user in lecture.participants.all()}
        return response.Response(data, status=status.HTTP_200_OK)


class LessonRetrieveView(RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LessonDetailSerializer

    def get_object(self):
        lecture_slug = self.kwargs["lecture_slug"]
        lesson_slug = self.kwargs["lesson_slug"]
        return Lesson.objects.get(lecture__slug=lecture_slug, slug=lesson_slug)


class LectureResourceDownload(RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        lecture_slug = self.kwargs["lecture_slug"]
        resource_uuid = self.kwargs["resource_uuid"]
        resource = LectureResource.objects.get(
            lecture__slug=lecture_slug, id=resource_uuid
        )
        return sendfile(request, resource.file.path, attachment=True)


class LessonResourceDownload(RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        lecture_slug = self.kwargs["lecture_slug"]
        lesson_slug = self.kwargs["lesson_slug"]
        resource_uuid = self.kwargs["resource_uuid"]
        resource = LessonResource.objects.get(
            lesson__lecture__slug=lecture_slug,
            lesson__slug=lesson_slug,
            id=resource_uuid,
        )
        return sendfile(request, resource.file.path, attachment=True)
