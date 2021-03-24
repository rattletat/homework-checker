import django_rq
from rest_framework import permissions, response, status
from rest_framework.exceptions import ParseError
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView
from sendfile import sendfile

from ..helpers import generate_sha1
from ..models import Exercise, ExerciseResource, Submission
from ..tasks import run_tests
from .serializers import (
    ExerciseSerializer,
    SubmissionListSerializer,
    SubmissionSerializer,
)
# from django.db.models import Max, Sum, Count
from collections import defaultdict


class ExerciseListView(ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ExerciseSerializer

    def get_queryset(self):
        lecture_slug = self.kwargs["lecture_slug"]
        lesson_slug = self.kwargs["lesson_slug"]
        return Exercise.objects.filter(
            lesson__lecture__slug=lecture_slug, lesson__slug=lesson_slug
        )


class ExerciseSubmitView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_class = FileUploadParser

    def post(self, request, exercise_id):
        if "file" not in request.data:
            raise ParseError("Empty content")

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
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SubmissionListSerializer

    def get_queryset(self):
        exercise_id = self.kwargs["exercise_id"]
        return Submission.objects.filter(
            user=self.request.user.id, exercise=exercise_id
        ).order_by("-created")[:5]


class ExercisesStatus(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, lecture_slug, lesson_slug):
        exercises = Exercise.objects.filter(
            lesson__lecture__slug=lecture_slug,
            lesson__slug=lesson_slug,
        )
        data = {}
        for exercise in exercises:
            submissions = Submission.objects.filter(
                exercise=exercise, user=request.user
            )
            data[exercise.slug] = max(map(lambda s: s.score, submissions), default=0)

        return response.Response(data, status=status.HTTP_200_OK)


# Todo
# class LectureStatisticsView(APIView):
#     permission_classes = [permissions.AllowAny]

#     def get(self, request, lecture_slug):
#         """ Returns all non-null scores anonymized. """

#         rows = (
#             Submission.objects.filter(
#                 exercise__lesson__lecture__slug=lecture_slug,
#                 score__isnull=False,
#                 # score__gt=0,
#                 exercise__rated=True,
#             )
#             .values("exercise", "user")
#             .annotate(max_score=Max("score"))
#             .values("user", "max_score")
#         )
#         scores = defaultdict(int)
#         for row in rows:
#             scores[row['user']] += row['max_score']

#         # f = models.Q()
#             # .values("user", "max_exercise_score")
#             # .aggregate(total_user_score=Sum("max_exercise_score"))
#         # .values("total_score")
#         # .annotate(user_count=Count("user"))
#         # )

#         return response.Response(
#             {"distribution", max_scores}, status=status.HTTP_200_OK
#         )
