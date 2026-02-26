from rest_framework.permissions import BasePermission, SAFE_METHODS
from profiles_app.models import Profile


class IsAuthenticatedCustomerForCreate(BasePermission):
    """
    - GET: jeder authentifizierte User darf lesen
    - POST: nur Customer darf erstellen
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return bool(request.user and request.user.is_authenticated)

        if not (request.user and request.user.is_authenticated):
            return False

        profile = getattr(request.user, "profile", None)
        return bool(profile and profile.role == Profile.ROLE_CUSTOMER)


class IsReviewerOwner(BasePermission):
    """
    - PATCH/DELETE: nur Ersteller der Bewertung (reviewer)
    - GET Detail: jeder Auth-User darf lesen
    """
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return bool(request.user and request.user.is_authenticated)
        return obj.reviewer == request.user