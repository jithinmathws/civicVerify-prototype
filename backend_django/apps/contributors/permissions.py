from rest_framework.permissions import BasePermission
from apps.contributors.models import Contributor


class IsContributorOwner(BasePermission):
    """
    Allows access only to the owning contributor.
    """

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_authenticated
            and isinstance(obj, Contributor)
            and obj.user == request.user
        )


class IsActiveContributor(BasePermission):
    """
    Allows access only if the requesting user is an active contributor.
    """

    def has_permission(self, request, view):
        user = request.user
        return (
            user.is_authenticated
            and hasattr(user, "contributor_profile")
            and user.contributor_profile.is_active
        )


class IsTargetContributorActive(BasePermission):
    """
    Allows access only if the target contributor is active.
    """

    def has_object_permission(self, request, view, obj):
        return getattr(obj, "is_active", False)