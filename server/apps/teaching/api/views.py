from apps.homework.models import Exercise
from rest_framework import permissions, response, status
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from sendfile import sendfile

from ..models import Lecture, LectureResource, Lesson, LessonResource, RegistrationCode
from .serializers import LessonDetailSerializer


class LectureRegister(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            code = RegistrationCode.objects.get(code=kwargs["registration_code"])
        except RegistrationCode.DoesNotExist:
            return response.Response({"detail": "Not a valid registration code!"}, status=status.HTTP_404_NOT_FOUND)
        code.lecture.participants.add(request.user)
        code.lecture.save()
        return response.Response(status=status.HTTP_200_OK)


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
        resource_id = self.kwargs["resource_id"]
        resource = LectureResource.objects.get(lecture__slug=lecture_slug, id=resource_id)
        return sendfile(request, resource.file.path, attachment=True)


class LessonResourceDownload(RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        lecture_slug = self.kwargs["lecture_slug"]
        lesson_slug = self.kwargs["lesson_slug"]
        resource_id = self.kwargs["resource_id"]
        resource = LessonResource.objects.get(
            lesson__lecture__slug=lecture_slug,
            lesson__slug=lesson_slug,
            id=resource_id,
        )
        return sendfile(request, resource.file.path, attachment=True)
