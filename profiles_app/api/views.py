from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from profiles_app.models import Profile
from .permissions import IsProfileOwner
from .serializers import ProfileSerializer


from django.shortcuts import get_object_or_404

class ProfileDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated, IsProfileOwner]

    def get_object(self):
        user_id = self.kwargs["pk"]  # pk ist User-ID (laut Doku)
        obj = get_object_or_404(Profile.objects.select_related("user"), user_id=user_id)

        # 🔥 DAS ist der wichtige Teil:
        self.check_object_permissions(self.request, obj)

        return obj
        
class BusinessProfilesListView(generics.ListAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Profile.objects.select_related("user").filter(role=Profile.ROLE_BUSINESS)


class CustomerProfilesListView(generics.ListAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Profile.objects.select_related("user").filter(role=Profile.ROLE_CUSTOMER)