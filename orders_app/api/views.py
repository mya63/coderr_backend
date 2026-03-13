from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from orders_app.api.permissions import IsBusinessUser, IsCustomerUser
from orders_app.api.serializers import (
    OrderCreateSerializer,
    OrderSerializer,
    OrderStatusUpdateSerializer,
)
from orders_app.models import Order


class OrderListCreateView(generics.ListCreateAPIView):
    """
    List all orders related to the authenticated user
    or create a new order as a customer.
    """

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Return all orders where the current user is either
        the customer or the business user.
        """
        user = self.request.user
        return Order.objects.filter(
            Q(customer_user=user) | Q(business_user=user)
        ).distinct()

    def get_serializer_class(self):
        """
        Return the serializer used for the current request method.
        """
        if self.request.method == "POST":
            return OrderCreateSerializer
        return OrderSerializer

    def create(self, request, *args, **kwargs):
        """
        Create a new order for authenticated customer users only.
        """
        permission = IsCustomerUser()
        if not permission.has_permission(request, self):
            return Response(
                {"detail": "Not allowed."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()

        return Response(
            OrderSerializer(order).data,
            status=status.HTTP_201_CREATED,
        )


class OrderPatchDeleteView(generics.GenericAPIView):
    """
    Update the status of an order as the assigned business user
    or delete an order as a staff user.
    """

    queryset = Order.objects.all()
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        """
        Update the status of an order.
        Only the assigned business user is allowed to perform this action.
        """
        order = self.get_object()
        permission = IsBusinessUser()

        if not permission.has_permission(request, self):
            return Response(
                {"detail": "Not allowed."},
                status=status.HTTP_403_FORBIDDEN,
            )

        if order.business_user != request.user:
            return Response(
                {"detail": "Not allowed."},
                status=status.HTTP_403_FORBIDDEN,
            )

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
        """
        Delete an order.
        Only staff users are allowed to perform this action.
        """
        if not request.user.is_staff:
            return Response(
                {"detail": "Not allowed."},
                status=status.HTTP_403_FORBIDDEN,
            )

        order = self.get_object()
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class OrderCountView(generics.GenericAPIView):
    """
    Return the number of in-progress orders for a specific business user.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, business_user_id: int):
        """
        Return the count of active orders for the given business user.
        """
        if not User.objects.filter(id=business_user_id).exists():
            return Response(
                {"detail": "Business user not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        order_count = Order.objects.filter(
            business_user_id=business_user_id,
            status=Order.STATUS_IN_PROGRESS,
        ).count()

        return Response(
            {"order_count": order_count},
            status=status.HTTP_200_OK,
        )


class CompletedOrderCountView(generics.GenericAPIView):
    """
    Return the number of completed orders for a specific business user.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, business_user_id: int):
        """
        Return the count of completed orders for the given business user.
        """
        if not User.objects.filter(id=business_user_id).exists():
            return Response(
                {"detail": "Business user not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        completed_order_count = Order.objects.filter(
            business_user_id=business_user_id,
            status=Order.STATUS_COMPLETED,
        ).count()

        return Response(
            {"completed_order_count": completed_order_count},
            status=status.HTTP_200_OK,
        )