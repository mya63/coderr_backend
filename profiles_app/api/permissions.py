from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsProfileOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        # GET/HEAD/OPTIONS erlauben
        if request.method in SAFE_METHODS:
            return True
        # PATCH/PUT/DELETE nur Owner
        return obj.user == request.user