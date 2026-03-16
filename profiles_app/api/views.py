from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .filters import (
    get_business_profiles,
    get_customer_profiles,
    get_profile_by_user_id,
)
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
        obj = get_profile_by_user_id(self.kwargs["pk"])
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
        return get_business_profiles()


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
        return get_customer_profiles()