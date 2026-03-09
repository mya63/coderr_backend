from django.contrib.auth.models import User   
from rest_framework import serializers
from rest_framework.reverse import reverse   
from offers_app.models import Offer, OfferDetail


class OfferDetailSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)  # allow id in PATCH payload

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
# : Nur für GET-Listenansicht: Details als {id, url}
class OfferDetailLinkSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()  

    class Meta:
        model = OfferDetail
        fields = ["id", "url"]  

    def get_url(self, obj):
        request = self.context.get("request")
        # : baut "/api/offerdetails/<id>/" (falls du Names hast, können wir reverse nehmen)
        return request.build_absolute_uri(f"/api/offerdetails/{obj.id}/") if request else f"/api/offerdetails/{obj.id}/"


# : User Details laut Doku
class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username"]


# : READ Serializer (GET): Doku-Format
class OfferReadSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    details = OfferDetailLinkSerializer(many=True, read_only=True)  # : Links statt volle Details
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
        return getattr(obj, "min_price", None)

    def get_min_delivery_time(self, obj):
        return getattr(obj, "min_delivery_time", None)

    def get_user_details(self, obj):
        if not obj.user:
            return {"first_name": "", "last_name": "", "username": ""}
        return {
            "first_name": obj.user.first_name,
            "last_name": obj.user.last_name,
            "username": obj.user.username,
        }
    
    # : Doku Serializer für GET /api/offers/{id}/ (OHNE user_details)
class OfferRetrieveSerializer(serializers.ModelSerializer):
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
        prices = obj.details.values_list("price", flat=True)
        return min(prices) if prices else None

    def get_min_delivery_time(self, obj):
        days = obj.details.values_list("delivery_time_in_days", flat=True)
        return min(days) if days else None


class OfferWriteSerializer(serializers.ModelSerializer):
    # PATCH/POST must accept full details and return full details with ids
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
        # POST must contain exactly 3 offer details
        request = self.context.get("request")

        if request and request.method == "POST":
            details = attrs.get("details", [])
            if len(details) != 3:
                raise serializers.ValidationError(
                    {"details": "An offer must contain exactly 3 details."}
                )

        return attrs

    def create(self, validated_data):
        # Create offer with nested details
        details_data = validated_data.pop("details", [])
        request = self.context.get("request")

        offer = Offer.objects.create(
            user=request.user,
            **validated_data
        )

        for detail_data in details_data:
            OfferDetail.objects.create(offer=offer, **detail_data)

        return offer

    def update(self, instance, validated_data):
        # PATCH updates details by offer_type, not by detail id
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
                        offer_type=offer_type
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