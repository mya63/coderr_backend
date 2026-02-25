from rest_framework.permissions import BasePermission
from profiles_app.models import Profile


class IsCustomerUser(BasePermission):
    def has_permission(self, request, view):
        profile = getattr(request.user, "profile", None)
        return bool(profile and profile.role == Profile.ROLE_CUSTOMER)


class IsBusinessUser(BasePermission):
    def has_permission(self, request, view):
        profile = getattr(request.user, "profile", None)
        return bool(profile and profile.role == Profile.ROLE_BUSINESS)