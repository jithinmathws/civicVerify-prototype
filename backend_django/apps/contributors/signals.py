from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Contributor


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_contributor_profile(sender, instance, created, **kwargs):
    if created:
        Contributor.objects.get_or_create(user=instance)


'''
from django.db import models
from apps.common.models import TimeStampedModel
from .models import ContributorProfile

class ContributionSignal(TimeStampedModel):
    contributor = models.ForeignKey(
        ContributorProfile, on_delete=models.CASCADE, related_name="signals"
    )

    claim_id = models.UUIDField()
    evidence_count = models.PositiveIntegerField(default=0)

    verification_outcome = models.CharField(
        max_length=20,
        choices=[
            ("pending", "Pending"),
            ("verified", "Verified"),
            ("rejected", "Rejected"),
        ],
    )

    confidence_score = models.FloatField(null=True, blank=True)


from django.db import models
from apps.common.models import TimeStampedModel
from apps.contributors.models import Contributor
from apps.claims.models import Claim  # assuming you have a Claim model


class ContributionSignal(TimeStampedModel):
    """
    Tracks contributor activity and verification outcomes for claims.
    Useful for analytics, reward weighting, and moderation insights.
    """

    contributor = models.ForeignKey(
        Contributor,
        on_delete=models.CASCADE,
        related_name="signals"
    )

    claim = models.ForeignKey(
        Claim,
        on_delete=models.CASCADE,
        related_name="contribution_signals"
    )

    evidence_count = models.PositiveIntegerField(default=0)

    verification_outcome = models.CharField(
        max_length=20,
        choices=[
            ("pending", "Pending"),
            ("verified", "Verified"),
            ("rejected", "Rejected"),
        ],
        default="pending"
    )

    confidence_score = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.contributor.display_name} → {self.claim.id} ({self.verification_outcome})"
        '''