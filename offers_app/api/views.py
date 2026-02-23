from rest_framework import generics, permissions
from offers_app.models import Offer, OfferDetail
from .serializers import OfferSerializer, OfferDetailSerializer
from .permissions import IsBusinessUser, IsOwner


# GET /api/offers/  +  POST /api/offers/
class OfferListCreateView(generics.ListCreateAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.IsAuthenticated(), IsBusinessUser()]
        return [permissions.IsAuthenticated()]

    def get_serializer_context(self):  # MYA: request sicher an serializer geben
        return {"request": self.request}    


# GET/PATCH/DELETE /api/offers/{id}/
class OfferDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]


# GET /api/offerdetails/{id}/
class OfferDetailSingleView(generics.RetrieveAPIView):
    queryset = OfferDetail.objects.all()
    serializer_class = OfferDetailSerializer
    permission_classes = [permissions.IsAuthenticated]