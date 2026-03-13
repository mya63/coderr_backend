from rest_framework import serializers

from profiles_app.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    """
    Serialize profile data and expose selected related user fields.
    """

    user = serializers.IntegerField(source="user.id", read_only=True)
    username = serializers.CharField(source="user.username", read_only=True)
    email = serializers.EmailField(source="user.email", required=False)
    type = serializers.CharField(source="role", read_only=True)
    file = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = [
            "user",
            "username",
            "first_name",
            "last_name",
            "file",
            "location",
            "tel",
            "description",
            "working_hours",
            "type",
            "email",
            "created_at",
        ]
        read_only_fields = ["user", "username", "type", "file", "created_at"]

    def get_file(self, obj):
        """
        Return the file URL or an empty string if no file exists.
        """
        if obj.file and hasattr(obj.file, "url"):
            return obj.file.url
        return ""

    def update(self, instance, validated_data):
        """
        Update profile data and synchronize the related user email.
        """
        user_data = validated_data.pop("user", {})

        if "email" in user_data:
            instance.user.email = user_data["email"]
            instance.user.save()

        return super().update(instance, validated_data)