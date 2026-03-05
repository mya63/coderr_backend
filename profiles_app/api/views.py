from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from profiles_app.models import Profile
from .permissions import IsProfileOwner
from .serializers import ProfileSerializer


class ProfileDetailView(generics.RetrieveUpdateAPIView):
    # Serializer used for retrieving and updating profile data
    serializer_class = ProfileSerializer

    # User must be authenticated and owner of the profile
    permission_classes = [IsAuthenticated, IsProfileOwner]

    def get_object(self):
        # pk represents the user_id according to API specification
        user_id = self.kwargs["pk"]

        # Optimize query by loading related user in same query
        obj = get_object_or_404(
            Profile.objects.select_related("user"),
            user_id=user_id
        )

        # Explicitly check object-level permissions
        self.check_object_permissions(self.request, obj)

        return obj


class BusinessProfilesListView(generics.ListAPIView):
    # List all business profiles
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Return profiles with role = business
        return Profile.objects.select_related("user").filter(
            role=Profile.ROLE_BUSINESS
        )


class CustomerProfilesListView(generics.ListAPIView):
    # List all customer profiles
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Return profiles with role = customer
        return Profile.objects.select_related("user").filter(
            role=Profile.ROLE_CUSTOMER
        )