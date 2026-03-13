from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from profiles_app.models import Profile
from .permissions import IsProfileOwner
from .serializers import ProfileSerializer


class ProfileDetailView(generics.RetrieveUpdateAPIView):
    """
    Retrieve or update a specific user profile.

    The authenticated user must be the owner of the profile.
    """

    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated, IsProfileOwner]

    def get_object(self):
        """
        Return the profile associated with the provided user_id.
        """
        user_id = self.kwargs["pk"]

        obj = get_object_or_404(
            Profile.objects.select_related("user"),
            user_id=user_id
        )

        self.check_object_permissions(self.request, obj)
        return obj


class BusinessProfilesListView(generics.ListAPIView):
    """
    List all profiles that belong to business users.
    """

    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Return profiles with the business role.
        """
        return Profile.objects.select_related("user").filter(
            role=Profile.ROLE_BUSINESS
        )


class CustomerProfilesListView(generics.ListAPIView):
    """
    List all profiles that belong to customer users.
    """

    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Return profiles with the customer role.
        """
        return Profile.objects.select_related("user").filter(
            role=Profile.ROLE_CUSTOMER
        )