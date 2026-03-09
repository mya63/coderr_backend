from math import perm

from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import generics, request, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from orders_app.models import Order
from orders_app.api.permissions import IsCustomerUser, IsBusinessUser
from orders_app.api.serializers import (
    OrderSerializer,
    OrderCreateSerializer,
    OrderStatusUpdateSerializer,
)


class OrderListCreateView(generics.ListCreateAPIView):
    # Only authenticated users can access orders
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Return orders where user is either customer or business partner
        user = self.request.user
        return Order.objects.filter(
            Q(customer_user=user) | Q(business_user=user)
        ).distinct()

    def get_serializer_class(self):
        # Use dedicated serializer for order creation
        if self.request.method == "POST":
            return OrderCreateSerializer
        return OrderSerializer

    def create(self, request, *args, **kwargs):
        # Only customers are allowed to create orders
        perm = IsCustomerUser()
        if not perm.has_permission(request, self):
            return Response({"detail": "Not allowed."}, status=status.HTTP_403_FORBIDDEN)

        # Validate request data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Create order instance
        order = serializer.save()

        # Return full order representation
        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)


class OrderPatchDeleteView(generics.GenericAPIView):
    queryset = Order.objects.all()
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        order = self.get_object()

        perm = IsBusinessUser()
        if not perm.has_permission(request, self):
            return Response({"detail": "Not allowed."}, status=status.HTTP_403_FORBIDDEN)

        if order.business_user != request.user:
            return Response({"detail": "Not allowed."}, status=status.HTTP_403_FORBIDDEN)

        if "status" not in request.data:
            return Response(
            {"status": ["This field is required."]},
            status=status.HTTP_400_BAD_REQUEST,
        )

        serializer = OrderStatusUpdateSerializer(order, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        order.refresh_from_db()
        return Response(OrderSerializer(order).data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        # Only admin/staff users can delete orders
        if not request.user.is_staff:
            return Response({"detail": "Not allowed."}, status=status.HTTP_403_FORBIDDEN)

        order = self.get_object()
        order.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class OrderCountView(generics.GenericAPIView):
    # Authenticated users can query order counts
    permission_classes = [IsAuthenticated]

    def get(self, request, business_user_id: int):
        # Ensure business user exists
        if not User.objects.filter(id=business_user_id).exists():
            return Response({"detail": "Business user not found."}, status=status.HTTP_404_NOT_FOUND)

        # Count active orders for business user
        order_count = Order.objects.filter(
            business_user_id=business_user_id,
            status=Order.STATUS_IN_PROGRESS,
        ).count()

        return Response({"order_count": order_count}, status=status.HTTP_200_OK)


class CompletedOrderCountView(generics.GenericAPIView):
    # Authenticated users can query completed order counts
    permission_classes = [IsAuthenticated]

    def get(self, request, business_user_id: int):
        # Ensure business user exists
        if not User.objects.filter(id=business_user_id).exists():
            return Response({"detail": "Business user not found."}, status=status.HTTP_404_NOT_FOUND)

        # Count completed orders for business user
        completed_order_count = Order.objects.filter(
            business_user_id=business_user_id,
            status=Order.STATUS_COMPLETED,
        ).count()

        return Response({"completed_order_count": completed_order_count}, status=status.HTTP_200_OK)