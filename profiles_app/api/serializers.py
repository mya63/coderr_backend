from rest_framework import serializers
from profiles_app.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    # user soll als ID rauskommen
    user = serializers.IntegerField(source="user.id", read_only=True)

    username = serializers.CharField(source="user.username", read_only=True)

    # MYA: email muss PATCH-bar sein (kommt aus user.email)
    email = serializers.EmailField(source="user.email", required=False)

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
        # MYA: email darf NICHT read_only sein, sonst kann PATCH es nicht ändern
        read_only_fields = ["user", "username", "type", "file", "created_at"]

    def get_file(self, obj):
        if obj.file and hasattr(obj.file, "url"):
            return obj.file.url
        return ""

    # MYA: PATCH muss user.email aktualisieren (email liegt am User, nicht am Profile)
    def update(self, instance, validated_data):
        user_data = validated_data.pop("user", {})

        if "email" in user_data:
            instance.user.email = user_data["email"]
            instance.user.save()

        return super().update(instance, validated_data)