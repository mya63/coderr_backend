from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from reviews_app.api.permissions import (
    IsAuthenticatedCustomerForCreate,
    IsReviewerOwner,
)
from reviews_app.api.serializers import ReviewSerializer
from reviews_app.models import Review


class ReviewListCreateView(generics.ListCreateAPIView):
    """
    List reviews or create a new review.

    Authenticated users can access this endpoint.
    Creating a review additionally requires a customer user.
    """

    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated, IsAuthenticatedCustomerForCreate]

    def get_queryset(self):
        """
        Return reviews filtered and ordered by query parameters.
        """
        queryset = Review.objects.all()

        business_user_id = self.request.query_params.get("business_user_id")
        reviewer_id = self.request.query_params.get("reviewer_id")

        if business_user_id:
            queryset = queryset.filter(business_user_id=business_user_id)
        if reviewer_id:
            queryset = queryset.filter(reviewer_id=reviewer_id)

        ordering = self.request.query_params.get("ordering")
        if ordering == "rating":
            queryset = queryset.order_by("-rating", "-updated_at")
        elif ordering == "updated_at":
            queryset = queryset.order_by("-updated_at")

        return queryset

    def get_serializer_context(self):
        """
        Return serializer context including the current request.
        """
        context = super().get_serializer_context()
        context["request"] = self.request
        return context


class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a single review.

    Only the review owner is allowed to update or delete.
    """

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated, IsReviewerOwner]

    def get_serializer_context(self):
        """
        Return serializer context including the current request.
        """
        context = super().get_serializer_context()
        context["request"] = self.request
        return context