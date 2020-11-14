from rest_framework.generics import ListAPIView
from rest_framework import status, response, permissions
from ..models import Exercise, Submission
from .serializers import ExerciseSerializer

from rest_framework.exceptions import ParseError
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView


class ExerciseListView(ListAPIView):
    queryset = Exercise.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ExerciseSerializer

    def get_queryset(self):
        lecture_slug = self.kwargs["lecture_slug"]
        lesson_slug = self.kwargs["lesson_slug"]
        return self.queryset.filter(
            lesson__lecture__slug=lecture_slug, lesson__slug=lesson_slug
        )


class ExerciseSubmitView(APIView):
    parser_class = (FileUploadParser)

    def post(self, request, exercise_id):
        if 'file' not in request.data:
            raise ParseError("Empty content")

        f = request.data['file']
        print(f)
        print(exercise_id)
        return response.Response({}, status=status.HTTP_200_OK)
