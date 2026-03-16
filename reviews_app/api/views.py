from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from reviews_app.api.filters import get_filtered_reviews 
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
        return get_filtered_reviews(self.request)


class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a single review.

    Only the review owner is allowed to update or delete.
    """

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated, IsReviewerOwner]