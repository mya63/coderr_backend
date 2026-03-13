from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers

User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    """
    Serialize user registration data and create a new user account.
    """

    password = serializers.CharField(write_only=True, min_length=8)
    type = serializers.ChoiceField(
        choices=["customer", "business"],
        write_only=True,
    )

    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "type"]

    def create(self, validated_data):
        """
        Create and return a new user instance.
        """
        validated_data.pop("type", None)
        return User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email", ""),
            password=validated_data["password"],
        )


class LoginSerializer(serializers.Serializer):
    """
    Validate login credentials and return the authenticated user.
    """

    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        """
        Authenticate the user with the provided credentials.
        """
        user = authenticate(
            username=attrs["username"],
            password=attrs["password"],
        )
        if not user:
            raise serializers.ValidationError("Invalid credentials.")

        attrs["user"] = user
        return attrs