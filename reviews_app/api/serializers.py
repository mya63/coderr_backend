from django.db import IntegrityError
from rest_framework import serializers

from reviews_app.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    """
    Serialize review data for create, read, update, and delete operations.
    """

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
        """
        Prevent users from reviewing themselves.
        """
        request = self.context["request"]
        if business_user == request.user:
            raise serializers.ValidationError("You cannot review yourself.")
        return business_user

    def validate(self, attrs):
        """
        Ensure that a user can submit only one review
        per business user.
        """
        request = self.context["request"]
        reviewer = request.user
        business_user = attrs.get("business_user")

        if self.instance is None and business_user:
            if Review.objects.filter(
                reviewer=reviewer,
                business_user=business_user,
            ).exists():
                raise serializers.ValidationError(
                    {
                        "business_user": (
                            "You already submitted a review "
                            "for this business user."
                        )
                    }
                )

        return attrs

    def create(self, validated_data):
        """
        Create a new review for the authenticated user.
        """
        request = self.context["request"]
        validated_data["reviewer"] = request.user

        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError(
                {
                    "business_user": (
                        "You already submitted a review "
                        "for this business user."
                    )
                }
            )

    def update(self, instance, validated_data):
        """
        Update rating and description of an existing review.
        """
        instance.rating = validated_data.get("rating", instance.rating)
        instance.description = validated_data.get(
            "description",
            instance.description,
        )
        instance.save()
        return instance