from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import LogInSerializer, UserSerializer


class SignUpView(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class LogInView(TokenObtainPairView):
    serializer_class = LogInSerializer
    permission_classes = [AllowAny]


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        response = {
            "full_name": request.user.full_name,
            "email": request.user.email,
            "identifier": request.user.identifier,
        }
        return Response(response, status=HTTP_200_OK)


class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        lectures = request.user.enrolled_lectures.all()
        attributes = ["title", "slug", "start", "end", "status"]
        enrolled_lectures = []
        for lecture in lectures:
            lecture_info = {attr: getattr(lecture, attr) for attr in attributes}
            score = lecture.get_score(request.user)
            lecture_info["score"] = score
            if scale:=lecture.grading_scale:
                lecture_info["grade"] = scale.get_grade(score)
            enrolled_lectures.append(lecture_info)
        
        return Response({"enrolled_lectures": enrolled_lectures}, status=HTTP_200_OK)
