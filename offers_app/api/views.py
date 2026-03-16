from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, permissions
from rest_framework.pagination import PageNumberPagination

from offers_app.models import OfferDetail
from .filters import (
    OfferFilter,
    get_annotated_offers,
    get_ordered_annotated_offers,
)
from .permissions import IsBusinessUser, IsOwner
from .serializers import (
    OfferDetailSerializer,
    OfferReadSerializer,
    OfferRetrieveSerializer,
    OfferWriteSerializer,
)


class OfferPagination(PageNumberPagination):
    """
    Page number pagination for offer list endpoints.
    """

    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class OfferListCreateView(generics.ListCreateAPIView):
    """
    List all offers or create a new offer.

    GET requests are public.
    POST requests require an authenticated business user.
    """

    pagination_class = OfferPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = OfferFilter
    search_fields = ["title", "description"]
    ordering_fields = ["updated_at", "min_price"]
    ordering = ["-updated_at"]

    def get_permissions(self):
        """
        Return permissions based on the current request method.
        """
        if self.request.method == "GET":
            return [permissions.AllowAny()]
        if self.request.method == "POST":
            return [permissions.IsAuthenticated(), IsBusinessUser()]
        return [permissions.IsAuthenticated()]

    def get_serializer_class(self):
        """
        Return the serializer used for the current request method.
        """
        if self.request.method == "GET":
            return OfferReadSerializer
        return OfferWriteSerializer

    def get_queryset(self):
        """
        Return all offers annotated with minimum price
        and minimum delivery time.
        """
        return get_ordered_annotated_offers()


class OfferDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a single offer.

    GET requests require authentication.
    PATCH and DELETE requests are restricted to the owner.
    """

    def get_queryset(self):
        return get_annotated_offers()

    def get_permissions(self):
        """
        Return permissions based on the current request method.
        """
        if self.request.method == "GET":
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated(), IsOwner()]

    def get_serializer_class(self):
        """
        Return the serializer used for the current request method.
        """
        if self.request.method == "GET":
            return OfferRetrieveSerializer
        return OfferWriteSerializer


class OfferDetailSingleView(generics.RetrieveAPIView):
    """
    Retrieve a single offer detail instance.
    """

    queryset = OfferDetail.objects.all()
    serializer_class = OfferDetailSerializer
    permission_classes = [permissions.IsAuthenticated]