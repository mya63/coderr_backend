from django.db import IntegrityError
from rest_framework import serializers
from reviews_app.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = [
            "id",
            "business_user",
            "reviewer",
            "rating",
            "description",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "reviewer", "created_at", "updated_at"]

    def validate_business_user(self, business_user):
        request = self.context["request"]
        if business_user == request.user:
            raise serializers.ValidationError("You cannot review yourself.")
        return business_user

    def validate(self, attrs):
        """
        Doku: Ein Benutzer kann nur eine Bewertung pro Geschäftsprofil abgeben.
        => reviewer + business_user muss unique sein
        """
        request = self.context["request"]
        reviewer = request.user
        business_user = attrs.get("business_user")

        # nur bei CREATE prüfen (bei PATCH bleibt business_user sowieso gleich)
        if self.instance is None and business_user:
            if Review.objects.filter(reviewer=reviewer, business_user=business_user).exists():
                raise serializers.ValidationError(
                    {"business_user": "You already submitted a review for this business user."}
                )

        return attrs

    def create(self, validated_data):
        request = self.context["request"]
        validated_data["reviewer"] = request.user

        try:
            return super().create(validated_data)
        except IntegrityError:
            # Safety-Net (Race condition)
            raise serializers.ValidationError(
                {"business_user": "You already submitted a review for this business user."}
            )
        
    def update(self, instance, validated_data):
        instance.rating = validated_data.get("rating", instance.rating)
        instance.description = validated_data.get("description", instance.description)
        instance.save()
        return instance    