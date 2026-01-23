from django.db.models import Q
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from apps.claims.models import Claim
from apps.claims.serializers.claim import (
    ClaimCreateSerializer,
    ClaimDetailSerializer,
    ClaimListSerializer,
)


class ClaimCreateView(CreateAPIView):
    serializer_class = ClaimCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, status=ClaimStatus.DRAFT)


class ClaimListView(ListAPIView):
    serializer_class = ClaimListSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Claim.objects.filter(
                Q(is_public=True) | Q(created_by=user)
            ).order_by("-created_at")
        return Claim.objects.filter(is_public=True).order_by("-created_at")



class ClaimDetailView(RetrieveAPIView):
    serializer_class = ClaimDetailSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Claim.objects.filter(
                Q(is_public=True) | Q(created_by=user)
            )
        return Claim.objects.filter(is_public=True)
