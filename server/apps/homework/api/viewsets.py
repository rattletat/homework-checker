from ..models import Exercise, Submission
from rest_framework.viewsets import ReadOnlyModelViewSet

from .serializers import (
    ExerciseDetailSerializer,
    ExerciseSerializer,
    SubmissionSerializer,
)


class ExerciseReadOnlyModelViewSet(ReadOnlyModelViewSet):
    queryset = Exercise.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ExerciseDetailSerializer
        else:
            return ExerciseSerializer


class SubmissionReadOnlyModelViewSet(ReadOnlyModelViewSet):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
