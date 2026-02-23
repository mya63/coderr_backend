from rest_framework import serializers
from profiles_app.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    # user soll als ID rauskommen
    user = serializers.IntegerField(source="user.id", read_only=True)

    username = serializers.CharField(source="user.username", read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)

    # Doku erwartet "type" → wir mappen intern role -> type
    type = serializers.CharField(source="role", read_only=True)

    # Doku erwartet "file" als String (URL oder "")
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
        read_only_fields = ["user", "username", "email", "type", "file", "created_at"]

    def get_file(self, obj):
        if obj.file and hasattr(obj.file, "url"):
            return obj.file.url
        return ""