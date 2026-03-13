from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from profiles_app.models import Profile
from .serializers import LoginSerializer, RegistrationSerializer


class RegistrationView(APIView):
    """
    Register a new user account and return an authentication token.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        """
        Validate input data, create a user and profile,
        and return the authentication token.
        """
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()
        role = serializer.validated_data["type"]

        Profile.objects.create(user=user, role=role)
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
    """
    Authenticate a user and return an authentication token.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        """
        Validate login credentials and return the user's token.
        """
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
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