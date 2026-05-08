from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from profiles_app.models import Profile

from .serializers import LoginSerializer, RegistrationSerializer
from .services import (
    register_user_with_profile,
    login_user_and_get_token,
    ensure_demo_users,
)

User = get_user_model()


class RegistrationView(APIView):
    """
    Register a new user account and return an authentication token.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()
        role = serializer.validated_data["type"]

        token = register_user_with_profile(user, role)

        return Response(
            {
                "token": token.key,
                "username": user.username,
                "email": user.email,
                "user_id": user.id,
            },
            status=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    """
    Authenticate a user and return an authentication token.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        ensure_demo_users()

        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        token = login_user_and_get_token(user)

        return Response(
            {
                "token": token.key,
                "username": user.username,
                "email": user.email,
                "user_id": user.id,
            },
            status=status.HTTP_200_OK,
        )