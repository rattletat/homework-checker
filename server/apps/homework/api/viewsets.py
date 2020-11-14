from ..models import Exercise, Submission
from rest_framework.viewsets import ReadOnlyModelViewSet

from .serializers import (
    SubmissionSerializer,
)


class SubmissionReadOnlyModelViewSet(ReadOnlyModelViewSet):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
