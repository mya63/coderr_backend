from django.db.models import Min
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, filters
from rest_framework.pagination import PageNumberPagination

from offers_app.models import Offer, OfferDetail
from .filters import OfferFilter
from .permissions import IsBusinessUser, IsOwner
from .serializers import (
    OfferReadSerializer,
    OfferRetrieveSerializer,
    OfferWriteSerializer,
    OfferDetailSerializer,
)


class OfferPagination(PageNumberPagination):
    # Page-based pagination with configurable page_size via query param
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class OfferListCreateView(generics.ListCreateAPIView):
    # GET: public list endpoint, POST: business-only creation endpoint
    pagination_class = OfferPagination

    # Enable filtering, full-text search, and ordering via query params
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = OfferFilter
    search_fields = ["title", "description"]
    ordering_fields = ["updated_at", "min_price"]
    ordering = ["-updated_at"]

    def get_permissions(self):
        # GET is public; POST requires authenticated business user
        if self.request.method == "GET":
            return [permissions.AllowAny()]
        if self.request.method == "POST":
            return [permissions.IsAuthenticated(), IsBusinessUser()]
        return [permissions.IsAuthenticated()]

    def get_serializer_class(self):
        # Use different serializer for read vs write operations
        if self.request.method == "GET":
            return OfferReadSerializer
        return OfferWriteSerializer

    def get_queryset(self):
        # Annotate min_price and min_delivery_time to support filters and ordering
        return (
            Offer.objects.all()
            .annotate(
                min_price=Min("details__price"),
                min_delivery_time=Min("details__delivery_time_in_days"),
            )
            .order_by("-updated_at")
        )

    def get_serializer_context(self):
        # Provide request context for serializer (e.g. absolute URLs)
        return {"request": self.request}


class OfferDetailView(generics.RetrieveUpdateDestroyAPIView):
    # Detail endpoint with annotated fields for consistent responses
    queryset = Offer.objects.all().annotate(
        min_price=Min("details__price"),
        min_delivery_time=Min("details__delivery_time_in_days"),
    )

    def get_permissions(self):
        # GET requires authentication; PATCH/DELETE restricted to owner
        if self.request.method == "GET":
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated(), IsOwner()]

    def get_serializer_class(self):
        # Use a dedicated serializer for retrieve response format
        if self.request.method == "GET":
            return OfferRetrieveSerializer
        return OfferWriteSerializer

    def get_serializer_context(self):
        return {"request": self.request}


class OfferDetailSingleView(generics.RetrieveAPIView):
    # Retrieve a single OfferDetail (authenticated users only)
    queryset = OfferDetail.objects.all()
    serializer_class = OfferDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_context(self):
        return {"request": self.request}