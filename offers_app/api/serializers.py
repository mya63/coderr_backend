from django.contrib.auth.models import User
from rest_framework import serializers

from offers_app.models import Offer, OfferDetail


class OfferDetailSerializer(serializers.ModelSerializer):
    """
    Serialize full offer detail objects for create and update operations.
    """

    id = serializers.IntegerField(required=False)

    class Meta:
        model = OfferDetail
        fields = [
            "id",
            "title",
            "revisions",
            "delivery_time_in_days",
            "price",
            "features",
            "offer_type",
        ]


class OfferDetailLinkSerializer(serializers.ModelSerializer):
    """
    Serialize offer detail references with id and detail endpoint URL.
    """

    url = serializers.SerializerMethodField()

    class Meta:
        model = OfferDetail
        fields = ["id", "url"]

    def get_url(self, obj):
        """
        Return the absolute or relative URL for an offer detail object.
        """
        request = self.context.get("request")
        if request:
            return request.build_absolute_uri(f"/api/offerdetails/{obj.id}/")
        return f"/api/offerdetails/{obj.id}/"


class UserDetailsSerializer(serializers.ModelSerializer):
    """
    Serialize selected public fields of a user.
    """

    class Meta:
        model = User
        fields = ["first_name", "last_name", "username"]


class OfferReadSerializer(serializers.ModelSerializer):
    """
    Serialize offer data for list responses.
    """

    user = serializers.PrimaryKeyRelatedField(read_only=True)
    details = OfferDetailLinkSerializer(many=True, read_only=True)
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()
    user_details = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        fields = [
            "id",
            "user",
            "title",
            "image",
            "description",
            "created_at",
            "updated_at",
            "details",
            "min_price",
            "min_delivery_time",
            "user_details",
        ]

    def get_min_price(self, obj):
        """
        Return the annotated minimum price value.
        """
        return getattr(obj, "min_price", None)

    def get_min_delivery_time(self, obj):
        """
        Return the annotated minimum delivery time value.
        """
        return getattr(obj, "min_delivery_time", None)

    def get_user_details(self, obj):
        """
        Return selected user details for the offer owner.
        """
        if not obj.user:
            return {
                "first_name": "",
                "last_name": "",
                "username": "",
            }

        return {
            "first_name": obj.user.first_name,
            "last_name": obj.user.last_name,
            "username": obj.user.username,
        }


class OfferRetrieveSerializer(serializers.ModelSerializer):
    """
    Serialize offer data for single offer retrieval.
    """

    user = serializers.PrimaryKeyRelatedField(read_only=True)
    details = OfferDetailLinkSerializer(many=True, read_only=True)
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        fields = [
            "id",
            "user",
            "title",
            "image",
            "description",
            "created_at",
            "updated_at",
            "details",
            "min_price",
            "min_delivery_time",
        ]

    def get_min_price(self, obj):
        """
        Return the minimum price across all offer details.
        """
        prices = obj.details.values_list("price", flat=True)
        return min(prices) if prices else None

    def get_min_delivery_time(self, obj):
        """
        Return the minimum delivery time across all offer details.
        """
        days = obj.details.values_list("delivery_time_in_days", flat=True)
        return min(days) if days else None


class OfferWriteSerializer(serializers.ModelSerializer):
    """
    Serialize offer data for create and update operations.
    """

    details = OfferDetailSerializer(many=True)

    class Meta:
        model = Offer
        fields = [
            "id",
            "title",
            "image",
            "description",
            "details",
        ]

    def validate(self, attrs):
        """
        Ensure that POST requests contain exactly three offer details.
        """
        request = self.context.get("request")

        if request and request.method == "POST":
            details = attrs.get("details", [])
            if len(details) != 3:
                raise serializers.ValidationError(
                    {"details": "An offer must contain exactly 3 details."}
                )

        return attrs

    def create(self, validated_data):
        """
        Create an offer with nested offer details.
        """
        details_data = validated_data.pop("details", [])
        request = self.context.get("request")

        offer = Offer.objects.create(
            user=request.user,
            **validated_data,
        )

        for detail_data in details_data:
            OfferDetail.objects.create(offer=offer, **detail_data)

        return offer

    def update(self, instance, validated_data):
        """
        Update an offer and its nested details by offer_type.
        """
        details_data = validated_data.pop("details", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if details_data is not None:
            for detail_data in details_data:
                offer_type = detail_data.get("offer_type")

                if not offer_type:
                    raise serializers.ValidationError(
                        {"details": "Each detail needs an offer_type."}
                    )

                try:
                    detail_obj = OfferDetail.objects.get(
                        offer=instance,
                        offer_type=offer_type,
                    )
                except OfferDetail.DoesNotExist:
                    raise serializers.ValidationError(
                        {
                            "details": (
                                f"Detail with offer_type='{offer_type}' "
                                f"does not belong to this offer."
                            )
                        }
                    )

                for attr, value in detail_data.items():
                    setattr(detail_obj, attr, value)
                detail_obj.save()

        return instance