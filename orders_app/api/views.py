from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from orders_app.models import Order
from orders_app.api.permissions import IsCustomerUser, IsBusinessUser
from orders_app.api.serializers import (
    OrderSerializer,
    OrderCreateSerializer,
    OrderStatusUpdateSerializer,
)


class OrderListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(customer_user=user) | Order.objects.filter(business_user=user)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return OrderCreateSerializer
        return OrderSerializer

    def create(self, request, *args, **kwargs):
        # Only customers can create orders (Doku)
        perm = IsCustomerUser()
        if not perm.has_permission(request, self):
            return Response({"detail": "Not allowed."}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()

        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)


class OrderPatchDeleteView(generics.GenericAPIView):
    queryset = Order.objects.all()
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        # Only business users can update status (Doku)
        perm = IsBusinessUser()
        if not perm.has_permission(request, self):
            return Response({"detail": "Not allowed."}, status=status.HTTP_403_FORBIDDEN)

        order = self.get_object()

        # Owner check: business user can only update own orders
        if order.business_user != request.user:
            return Response({"detail": "Not allowed."}, status=status.HTTP_403_FORBIDDEN)

        serializer = OrderStatusUpdateSerializer(order, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(OrderSerializer(order).data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        # Only admin/staff can delete (Doku)
        if not request.user.is_staff:
            return Response({"detail": "Not allowed."}, status=status.HTTP_403_FORBIDDEN)

        order = self.get_object()
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class OrderCountView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, business_user_id: int):
        if not User.objects.filter(id=business_user_id).exists():
            return Response({"detail": "Business user not found."}, status=status.HTTP_404_NOT_FOUND)

        order_count = Order.objects.filter(
            business_user_id=business_user_id,
            status=Order.STATUS_IN_PROGRESS,
        ).count()
        return Response({"order_count": order_count}, status=status.HTTP_200_OK)


class CompletedOrderCountView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, business_user_id: int):
        if not User.objects.filter(id=business_user_id).exists():
            return Response({"detail": "Business user not found."}, status=status.HTTP_404_NOT_FOUND)

        completed_order_count = Order.objects.filter(
            business_user_id=business_user_id,
            status=Order.STATUS_COMPLETED,
        ).count()
        return Response({"completed_order_count": completed_order_count}, status=status.HTTP_200_OK)