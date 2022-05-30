import django_rq
from apps.teaching.api.mixins import MultipleFieldLookupMixin
from apps.teaching.api.permissions import IsEnrolled, IsNotWaiting
from rest_framework import exceptions, parsers, response, status
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from sendfile import sendfile

from ..helpers import generate_sha1
from ..models import Exercise, Submission
from ..tasks import run_tests
from .permissions import isAuthor
from .serializers import (
    ExerciseSerializer,
    SubmissionListSerializer,
    SubmissionSerializer,
)


class ExerciseListView(ListAPIView):
    permission_classes = [IsEnrolled, IsNotWaiting]
    serializer_class = ExerciseSerializer

    def get_queryset(self):
        lecture_slug = self.kwargs["lecture_slug"]
        lesson_slug = self.kwargs["lesson_slug"]
        return Exercise.objects.filter(
            lesson__lecture__slug=lecture_slug, lesson__slug=lesson_slug
        )


class ExerciseSubmitView(APIView):
    permission_classes = [IsEnrolled, IsNotWaiting]
    parser_class = parsers.FileUploadParser

    def post(self, request, exercise_id):
        if "file" not in request.data:
            raise exceptions.ParseError("Empty content")

        exercise = Exercise.objects.get(id=exercise_id)
        file = request.FILES["file"]
        file_hash = generate_sha1(file)

        submission = Submission(exercise=exercise, user=request.user)
        serializer = SubmissionSerializer(
            submission,
            data={
                "exercise": exercise.id,
                "user": request.user.id,
                "file": file,
                "file_hash": file_hash,
            },
            context={"request": request},
        )

        if serializer.is_valid(raise_exception=True):
            submission = serializer.save()
            submission.full_clean()
            django_rq.enqueue(run_tests, submission)
            return response.Response({}, status=status.HTTP_200_OK)


class SubmissionListView(ListAPIView):
    serializer_class = SubmissionListSerializer

    def get_queryset(self):
        exercise_id = self.kwargs["exercise_id"]
        return Submission.objects.filter(
            user=self.request.user.id, exercise=exercise_id
        ).order_by("-created")[:5]


class SubmissionDownload(MultipleFieldLookupMixin, RetrieveAPIView):
    permission_classes = [isAuthor]
    lookup_fields = {
        "exercise_id": "exercise",
        "submission_id": "id",
    }
    queryset = Submission.objects.all()

    def get(self, request, *args, **kwargs):
        submission = self.get_object()
        return sendfile(request, submission.file.path, attachment=True)
