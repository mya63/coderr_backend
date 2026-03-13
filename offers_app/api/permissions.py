from rest_framework.permissions import BasePermission

from profiles_app.models import Profile


class IsBusinessUser(BasePermission):
    """
    Allow access only to users with the business role.
    """

    def has_permission(self, request, view):
        """
        Check whether the authenticated user has a business profile.
        """
        profile = getattr(request.user, "profile", None)
        if not profile:
            return False
        return profile.role == Profile.ROLE_BUSINESS


class IsOwner(BasePermission):
    """
    Allow access only to the owner of the object.
    """

    def has_object_permission(self, request, view, obj):
        """
        Check whether the current user owns the object.
        """
        return obj.user == request.user