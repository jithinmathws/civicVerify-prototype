from rest_framework.permissions import BasePermission


class IsClaimOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ("GET", "HEAD", "OPTIONS"):
            return True
        return obj.created_by == request.user

class IsClaimPublicOrOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.is_public:
            return True
        return obj.created_by == request.user

class IsClaimOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.created_by == request.user or request.user.is_staff

class CanCreateClaim(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and hasattr(request.user, "contributor_profile")

