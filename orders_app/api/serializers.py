from django.db import IntegrityError
from rest_framework import serializers

from offers_app.models import OfferDetail
from orders_app.api.filters import create_order_from_offer_detail
from orders_app.models import Order


class OrderSerializer(serializers.ModelSerializer):
    """
    Serialize full order data for read operations.
    """

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
    """
    Validate input data and create a new order
    from an existing offer detail.
    """

    offer_detail_id = serializers.IntegerField(write_only=True)

    def validate_offer_detail_id(self, value: int) -> int:
        """
        Ensure that the referenced offer detail exists.
        """
        if not OfferDetail.objects.filter(id=value).exists():
            raise serializers.ValidationError("OfferDetail not found.")
        return value

    def create(self, validated_data):
        
        request = self.context["request"]

        try:
            return create_order_from_offer_detail(
                validated_data["offer_detail_id"],
                request.user,
            )
        except IntegrityError:
            raise serializers.ValidationError(
                {"detail": "Invalid order data."}
            )


class OrderStatusUpdateSerializer(serializers.ModelSerializer):
    """
    Serialize and validate order status updates.
    """

    class Meta:
        model = Order
        fields = ["status"]

    def validate_status(self, value: str) -> str:
        """
        Ensure that the provided status is allowed.
        """
        allowed = {
            Order.STATUS_IN_PROGRESS,
            Order.STATUS_COMPLETED,
            Order.STATUS_CANCELLED,
        }
        if value not in allowed:
            raise serializers.ValidationError("Invalid status.")
        return value