from django.contrib.auth.models import User  # MYA
from rest_framework import serializers
from rest_framework.reverse import reverse  # MYA
from offers_app.models import Offer, OfferDetail


class OfferDetailSerializer(serializers.ModelSerializer):
    offer = serializers.PrimaryKeyRelatedField(read_only=True)  # MYA: offer wird serverseitig gesetzt

    class Meta:
        model = OfferDetail
        fields = "__all__"


# MYA: Nur für GET-Listenansicht: Details als {id, url}
class OfferDetailLinkSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()  # MYA

    class Meta:
        model = OfferDetail
        fields = ["id", "url"]  # MYA

    def get_url(self, obj):
        request = self.context.get("request")
        # MYA: baut "/api/offerdetails/<id>/" (falls du Names hast, können wir reverse nehmen)
        return request.build_absolute_uri(f"/api/offerdetails/{obj.id}/") if request else f"/api/offerdetails/{obj.id}/"


# MYA: User Details laut Doku
class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username"]


# MYA: READ Serializer (GET): Doku-Format
class OfferReadSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    details = OfferDetailLinkSerializer(many=True, read_only=True)  # MYA: Links statt volle Details
    min_price = serializers.SerializerMethodField()  # MYA
    min_delivery_time = serializers.SerializerMethodField()  # MYA
    user_details = serializers.SerializerMethodField()  # MYA

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
        prices = obj.details.values_list("price", flat=True)
        return min(prices) if prices else None

    def get_min_delivery_time(self, obj):
        days = obj.details.values_list("delivery_time_in_days", flat=True)
        return min(days) if days else None

    def get_user_details(self, obj):
        if not obj.user:
            return {"first_name": "", "last_name": "", "username": ""}
        return {
            "first_name": obj.user.first_name,
            "last_name": obj.user.last_name,
            "username": obj.user.username,
        }


# MYA: WRITE Serializer (POST/PATCH): akzeptiert volle Details
class OfferWriteSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    details = OfferDetailSerializer(many=True)

    class Meta:
        model = Offer
        fields = "__all__"

    def create(self, validated_data):
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
        details_data = validated_data.pop("details", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if details_data is not None:
            for detail_data in details_data:
                detail_id = detail_data.get("id", None)
                if detail_id:
                    detail_obj = OfferDetail.objects.get(id=detail_id, offer=instance)
                    for attr, value in detail_data.items():
                        if attr != "id":
                            setattr(detail_obj, attr, value)
                    detail_obj.save()

        return instance