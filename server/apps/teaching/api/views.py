from apps.homework.models import Exercise
from rest_framework import permissions, response, status
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from sendfile import sendfile

from ..models import (Lecture, LectureResource, Lesson, LessonResource,
                      RegistrationCode)
from .mixins import MultipleFieldLookupMixin
from .permissions import IsEnrolled, IsNotWaiting
from .serializers import (EnrolledLectureListSerializer,
                          LectureDetailSerializer, LessonDetailSerializer)


class EnrolledLectureListView(ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = EnrolledLectureListSerializer

    def get_queryset(self):
        return self.request.user.enrolled_lectures.all()


class LectureRetrieveView(RetrieveAPIView):
    permission_classes = [IsEnrolled, IsNotWaiting]
    serializer_class = LectureDetailSerializer
    lookup_field = "slug"
    queryset = Lecture.objects.all()


class LectureRegister(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            code = RegistrationCode.objects.get(code=kwargs["registration_code"])
        except RegistrationCode.DoesNotExist:
            return response.Response(
                {"detail": "Not a valid registration code!"},
                status=status.HTTP_404_NOT_FOUND,
            )
        if code.lecture in request.user.enrolled_lectures.all():
            return response.Response(
                {"detail": "You are already enrolled in this lecture!"},
                status=status.HTTP_409_CONFLICT,
            )
        code.lecture.participants.add(request.user)
        code.lecture.save()
        return response.Response(status=status.HTTP_200_OK)


class LessonRetrieveView(MultipleFieldLookupMixin, RetrieveAPIView):
    permission_classes = [IsEnrolled, IsNotWaiting]
    serializer_class = LessonDetailSerializer
    lookup_fields = {"lecture_slug": "lecture__slug", "lesson_slug": "slug"}
    queryset = Lesson.objects.all()


class LectureResourceDownload(MultipleFieldLookupMixin, RetrieveAPIView):
    permission_classes = [IsEnrolled, IsNotWaiting]
    lookup_fields = {"lecture_slug": "lecture__slug", "resource_id": "id"}
    queryset = LectureResource.objects.all()

    def get(self, request, *args, **kwargs):
        resource = self.get_object()
        return sendfile(request, resource.file.path, attachment=True)


class LessonResourceDownload(MultipleFieldLookupMixin, RetrieveAPIView):
    permission_classes = [IsEnrolled, IsNotWaiting]
    lookup_fields = {
        "lecture_slug": "lesson__lecture__slug",
        "lesson_slug": "lesson__slug",
        "resource_id": "id",
    }
    queryset = LessonResource.objects.all()

    def get(self, request, *args, **kwargs):
        resource = self.get_object()
        return sendfile(request, resource.file.path, attachment=True)
