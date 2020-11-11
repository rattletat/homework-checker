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


class StatusView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):

        response = {
            "full_name": request.user.full_name,
            "email": request.user.email,
            "identifier": request.user.identifier,
            "enrolled_lectures": map(str, request.user.enrolled_lectures.all()),
        }
        return Response(response, status=HTTP_200_OK)
