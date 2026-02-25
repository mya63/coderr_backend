from django.contrib.auth.models import User
from rest_framework import serializers

from orders_app.models import Order
from offers_app.models import OfferDetail


class OrderSerializer(serializers.ModelSerializer):
    customer_user = serializers.PrimaryKeyRelatedField(read_only=True)
    business_user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "customer_user",
            "business_user",
            "title",
            "revisions",
            "delivery_time_in_days",
            "price",
            "features",
            "offer_type",
            "status",
            "created_at",
            "updated_at",
        ]

class OrderCreateSerializer(serializers.Serializer):
    offer_detail_id = serializers.IntegerField(write_only=True)

    def validate_offer_detail_id(self, value: int) -> int:
        if not OfferDetail.objects.filter(id=value).exists():
            raise serializers.ValidationError("OfferDetail not found.")
        return value

    def create(self, validated_data):
        request = self.context["request"]
        offer_detail = OfferDetail.objects.select_related("offer", "offer__user").get(
            id=validated_data["offer_detail_id"]
        )

        offer = offer_detail.offer
        business_user = offer.user
        customer_user = request.user

        # Read fields robustly (in case OfferDetail differs slightly)
        revisions = getattr(offer_detail, "revisions", 0)
        delivery_time_in_days = getattr(offer_detail, "delivery_time_in_days", 0)
        price = getattr(offer_detail, "price", 0)
        features = getattr(offer_detail, "features", []) or []
        offer_type = getattr(offer_detail, "offer_type", "basic")
        title = getattr(offer, "title", "")

        order = Order.objects.create(
            customer_user=customer_user,
            business_user=business_user,
            offer_detail=offer_detail,
            title=title,
            revisions=revisions,
            delivery_time_in_days=delivery_time_in_days,
            price=price,
            features=features,
            offer_type=offer_type,
            status=Order.STATUS_IN_PROGRESS,
        )
        return order


class OrderStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["status"]

    def validate_status(self, value: str) -> str:
        allowed = {Order.STATUS_IN_PROGRESS, Order.STATUS_COMPLETED, Order.STATUS_CANCELLED}
        if value not in allowed:
            raise serializers.ValidationError("Invalid status.")
        return value