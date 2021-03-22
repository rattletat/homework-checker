from apps.homework.models import Exercise
from rest_framework import permissions, response, status
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from sendfile import sendfile

from ..models import Lecture, LectureResource, Lesson, LessonResource, RegistrationCode
from .permissions import IsEnrolled
from .mixins import MultipleFieldLookupMixin
from .serializers import (
    LectureDetailSerializer,
    LectureListSerializer,
    LessonDetailSerializer,
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

        return Response(
            {"enrolled_lectures": enrolled_lectures}, status=status.HTTP_200_OK
        )


class LectureRetrieveView(RetrieveAPIView):
    permission_classes = [IsEnrolled]
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
    permission_classes = [IsEnrolled]
    serializer_class = LessonDetailSerializer
    lookup_fields = {"lecture_slug": "lecture__slug", "lesson_slug": "slug"}
    queryset = Lesson.objects.all()


class LectureResourceDownload(MultipleFieldLookupMixin, RetrieveAPIView):
    permission_classes = [IsEnrolled]
    lookup_fields = {"lecture_slug": "lecture__slug", "resource_id": "id"}
    queryset = LectureResource.objects.all()

    def get(self, request, *args, **kwargs):
        resource = self.get_object()
        return sendfile(request, resource.file.path, attachment=True)


class LessonResourceDownload(MultipleFieldLookupMixin, RetrieveAPIView):
    permission_classes = [IsEnrolled]
    lookup_fields = {
        "lecture_slug": "lesson__lecture__slug",
        "lesson_slug": "lesson__slug",
        "resource_id": "id",
    }
    queryset = LessonResource.objects.all()

    def get(self, request, *args, **kwargs):
        resource = self.get_object()
        return sendfile(request, resource.file.path, attachment=True)
