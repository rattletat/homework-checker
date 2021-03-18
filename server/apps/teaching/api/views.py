from apps.homework.models import Exercise
from rest_framework import permissions, response, status
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from sendfile import sendfile

from ..models import Lecture, LectureResource, Lesson, LessonResource, RegistrationCode
from .serializers import (
    LessonDetailSerializer,
    LectureDetailSerializer,
    LectureListSerializer,
    LectureDetailSerializer,
)


class LectureListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        lectures = request.user.enrolled_lectures.all()
        attributes = ["title", "slug", "start", "end", "status"]
        enrolled_lectures = []
        for lecture in lectures:
            lecture_info = {attr: getattr(lecture, attr) for attr in attributes}
            score = lecture.get_score(request.user)
            lecture_info["score"] = score
            if scale := lecture.grading_scale:
                lecture_info["grade"] = scale.get_grade(score)
            enrolled_lectures.append(lecture_info)

        return Response({"enrolled_lectures": enrolled_lectures}, status=status.HTTP_200_OK)


class LectureRetrieveView(RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LectureDetailSerializer

    def get_object(self):
        lecture_slug = self.kwargs["lecture_slug"]
        return Lecture.objects.get(slug=lecture_slug)


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
        resource = LectureResource.objects.get(
            lecture__slug=lecture_slug, id=resource_id
        )
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
