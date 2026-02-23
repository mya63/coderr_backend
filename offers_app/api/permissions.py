from rest_framework.permissions import BasePermission
from profiles_app.models import Profile


class IsBusinessUser(BasePermission):
    def has_permission(self, request, view):
        profile = getattr(request.user, "profile", None)
        if not profile:
            return False
        return profile.role == Profile.ROLE_BUSINESS


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user