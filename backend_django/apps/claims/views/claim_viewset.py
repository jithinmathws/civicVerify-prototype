from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models import Q

from apps.claims.models import Claim
from apps.claims.serializers import ClaimCreateSerializer, ClaimDetailSerializer, ClaimListSerializer
from apps.claims.permissions import (
    IsClaimOwner,
    IsClaimPublicOrOwner,
    CanCreateClaim,
)

class ClaimViewSet(viewsets.ModelViewSet):
    queryset = Claim.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            return ClaimCreateSerializer
        if self.action == "list":
            return ClaimListSerializer
        return ClaimDetailSerializer

    def get_permissions(self):
        if self.action == "create":
            # Only authenticated contributors can create claims
            permission_classes = [IsAuthenticated, CanCreateClaim]
        elif self.action in ["update", "partial_update", "destroy"]:
            # Only the claim owner (or admin if you extend) can modify/delete
            permission_classes = [IsAuthenticated, IsClaimOwner]
        elif self.action == "retrieve":
            # Public claims are visible to all, private claims only to owner
            permission_classes = [IsClaimPublicOrOwner]
        elif self.action == "list":
            # Anyone can list public claims
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Claim.objects.filter(
                Q(is_public=True) | Q(created_by=user)
            ).order_by("-created_at")
        return Claim.objects.filter(is_public=True).order_by("-created_at")

    
