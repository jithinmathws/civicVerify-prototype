from rest_framework.generics import (
    RetrieveAPIView,
    RetrieveUpdateAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound
from apps.contributors.models import Contributor
from apps.contributors.serializers import (
    ContributorSelfSerializer,
    ContributorPublicSerializer,
)
from apps.contributors.permissions import (
    IsContributorOwner,
    IsActiveContributor,
    IsTargetContributorActive,
)

class MyContributorProfileView(RetrieveUpdateAPIView):
    """
    Retrieve or update the authenticated user's contributor profile.
    """
    serializer_class = ContributorSelfSerializer
    permission_classes = [
        IsAuthenticated,
        IsActiveContributor,
        IsContributorOwner,
    ]

    def get_object(self):
        try:
            return self.request.user.contributor_profile
        except Contributor.DoesNotExist:
            raise NotFound("Contributor profile not found.")

class PublicContributorDetailView(RetrieveAPIView):
    """
    Public read-only view of an active contributor.
    """
    queryset = Contributor.objects.filter(is_active=True)
    serializer_class = ContributorPublicSerializer
    permission_classes = [
        IsTargetContributorActive,
    ]

class MyContributorReputationView(APIView):
    """
    Returns reputation and contribution statistics for the contributor.
    """
    permission_classes = [
        IsAuthenticated,
        IsActiveContributor,
    ]

    def get(self, request):

        contributor = getattr(request.user, "contributor_profile", None)
        if not contributor:
            raise NotFound("Contributor profile not found.")

        recent_logs = ReputationLogSerializer(
            contributor.reputation_logs.order_by("-created_at")[:5],
            many=True
        ).data

        data = {
            "reputation_score": contributor.reputation_score,
            "total_logs": contributor.reputation_logs.count(),
            "recent_activity": recent_logs,
        }
        return Response(data)