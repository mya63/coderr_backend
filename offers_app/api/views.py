# offers_app/api/views.py

from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from django.db.models import Min  # MYA

from offers_app.models import Offer, OfferDetail
from .serializers import (
    OfferReadSerializer,      # MYA
    OfferWriteSerializer,     # MYA
    OfferDetailSerializer
)
from .permissions import IsBusinessUser, IsOwner


# MYA: Pagination wie Doku (PageNumberPagination + page_size Query)
class OfferPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


# GET /api/offers/  +  POST /api/offers/
class OfferListCreateView(generics.ListCreateAPIView):
    queryset = Offer.objects.all().order_by("-updated_at")
    pagination_class = OfferPagination

    # MYA: Filter/Search/Ordering laut Doku
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "description"]
    ordering_fields = ["updated_at", "min_price"]  # MYA: min_price ordering machen wir später sauber per Annotation
    ordering = ["-updated_at"]

    def get_permissions(self):
        # MYA: Doku -> LIST ist public
        if self.request.method == "GET":
            return [permissions.AllowAny()]

        # MYA: POST bleibt nur Business
        if self.request.method == "POST":
            return [permissions.IsAuthenticated(), IsBusinessUser()]

        return [permissions.IsAuthenticated()]

    # MYA: GET => Read Serializer, POST => Write Serializer
    def get_serializer_class(self):
        if self.request.method == "GET":
            return OfferReadSerializer
        return OfferWriteSerializer

    # MYA: creator_id Query Param
    def get_queryset(self):
        qs = Offer.objects.all().annotate(
            min_price=Min("details__price"),  # MYA
            min_delivery_time=Min("details__delivery_time_in_days"),  # MYA (optional aber passend zur Doku)
    )

        creator_id = self.request.query_params.get("creator_id")
        if creator_id:
            qs = qs.filter(user_id=creator_id)

        return qs.order_by("-updated_at")

    def get_serializer_context(self):
        return {"request": self.request}


# GET/PATCH/DELETE /api/offers/{id}/
class OfferDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Offer.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    # MYA: GET => Read Serializer, PATCH/PUT => Write Serializer
    def get_serializer_class(self):
        if self.request.method == "GET":
            return OfferReadSerializer
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