from rest_framework.status import HTTP_200_OK
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from ..models import Lecture


class LectureSignUp(APIView):
    permission_classes = [IsAuthenticated]
    lookup_field = "slug"

    def post(self, request, *args, **kwargs):
        lecture = Lecture.objects.get(slug=kwargs["slug"])
        lecture.participants.add(request.user)
        lecture.save()
        return Response({}, status=HTTP_200_OK)


class LectureStatus(APIView):
    permission_classes = [IsAuthenticated]
    lookup_field = "slug"

    def get(self, request, *args, **kwargs):
        lecture = Lecture.objects.get(slug=kwargs["slug"])
        response = {"registered": request.user in lecture.participants.all()}
        return Response(response, status=HTTP_200_OK)
