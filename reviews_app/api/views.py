from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from reviews_app.models import Review
from reviews_app.api.serializers import ReviewSerializer
from reviews_app.api.permissions import IsAuthenticatedCustomerForCreate, IsReviewerOwner


class ReviewListCreateView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated, IsAuthenticatedCustomerForCreate]

    def get_queryset(self):
        qs = Review.objects.all()

        # Filter
        business_user_id = self.request.query_params.get("business_user_id")
        reviewer_id = self.request.query_params.get("reviewer_id")

        if business_user_id:
            qs = qs.filter(business_user_id=business_user_id)
        if reviewer_id:
            qs = qs.filter(reviewer_id=reviewer_id)

        # Ordering (laut Doku: updated_at oder rating)
        ordering = self.request.query_params.get("ordering")
        if ordering == "rating":
            qs = qs.order_by("-rating", "-updated_at")
        elif ordering == "updated_at":
            qs = qs.order_by("-updated_at")

        return qs

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx["request"] = self.request
        return ctx


class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated, IsReviewerOwner]

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx["request"] = self.request
        return ctx