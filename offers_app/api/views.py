# offers_app/api/views.py

from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from django.db.models import Min  # MYA

from offers_app.models import Offer, OfferDetail
from .serializers import (
    OfferReadSerializer,
    OfferRetrieveSerializer,            # MYA
    OfferWriteSerializer,     # MYA
    OfferDetailSerializer
)
from .permissions import IsBusinessUser, IsOwner
from .filters import OfferFilter  # MYA


# MYA: Pagination wie Doku (PageNumberPagination + page_size Query)
class OfferPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


# GET /api/offers/  +  POST /api/offers/
class OfferListCreateView(generics.ListCreateAPIView):
    pagination_class = OfferPagination

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = OfferFilter  # MYA
    search_fields = ["title", "description"]
    ordering_fields = ["updated_at", "min_price"]
    ordering = ["-updated_at"]

    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.AllowAny()]
        if self.request.method == "POST":
            return [permissions.IsAuthenticated(), IsBusinessUser()]
        return [permissions.IsAuthenticated()]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return OfferReadSerializer
        return OfferWriteSerializer

    def get_queryset(self):
        # MYA: immer annotieren, damit Filter + ordering funktionieren
        return Offer.objects.all().annotate(
            min_price=Min("details__price"),
            min_delivery_time=Min("details__delivery_time_in_days"),
        ).order_by("-updated_at")

    def get_serializer_context(self):
        return {"request": self.request}

# GET/PATCH/DELETE /api/offers/{id}/
class OfferDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Offer.objects.all().annotate(
        min_price=Min("details__price"),  # MYA
        min_delivery_time=Min("details__delivery_time_in_days"),  # MYA
    )
    
    # MYA: Doku -> GET nur Auth erforderlich, PATCH/DELETE nur Owner
    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated(), IsOwner()]

    # MYA: Doku -> GET /api/offers/{id}/ ohne user_details
    def get_serializer_class(self):
        if self.request.method == "GET":
            return OfferRetrieveSerializer
        return OfferWriteSerializer

    def get_serializer_context(self):
        return {"request": self.request}

# GET /api/offerdetails/{id}/
class OfferDetailSingleView(generics.RetrieveAPIView):
    queryset = OfferDetail.objects.all()
    serializer_class = OfferDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_context(self):
        return {"request": self.request}