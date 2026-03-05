from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from profiles_app.models import Profile
from .serializers import LoginSerializer, RegistrationSerializer


class RegistrationView(APIView):
    # Public endpoint – registration does not require authentication
    permission_classes = [AllowAny]

    def post(self, request):
        # Validate incoming registration data
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Create user account
        user = serializer.save()

        # Create related profile with requested role ("customer" or "business")
        role = serializer.validated_data["type"]
        Profile.objects.create(user=user, role=role)

        # Create token for immediate authentication
        token, _ = Token.objects.get_or_create(user=user)

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
    # Public endpoint – login does not require authentication
    permission_classes = [AllowAny]

    def post(self, request):
        # Validate credentials via serializer
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Serializer returns the authenticated user
        user = serializer.validated_data["user"]

        # Reuse existing token or create a new one
        token, _ = Token.objects.get_or_create(user=user)

        return Response(
            {
                "token": token.key,
                "username": user.username,
                "email": user.email,
                "user_id": user.id,
            },
            status=status.HTTP_200_OK,
        )