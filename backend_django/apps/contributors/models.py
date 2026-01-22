from django.db import models
from django.conf import settings
from apps.common.models import TimeStampedModel
from django.db.models import F
from django.db import transaction

class Contributor(TimeStampedModel):
    """
    Represents a contributor in the CivicVerify platform.
    Extends the custom User model from user_auth.
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="contributor_profile",
    )

    display_name = models.CharField(max_length=100)
    bio = models.TextField(blank=True, null=True)

    reputation_score = models.FloatField(default=0.0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.display_name or self.user.email

    
    
    def adjust_reputation(self, change: float, reason: str):
        """
        Adjust contributor reputation and record an audit log.
        """
        with transaction.atomic():
            Contributor.objects.filter(pk=self.pk).update(
                reputation_score=F("reputation_score") + change
            )
            ReputationLog.objects.create(
                contributor=self,
                change=change,
                reason=reason,
            )


class ReputationLog(TimeStampedModel):
    """
    Audit log for reputation changes.
    """
    contributor = models.ForeignKey(
        Contributor,
        on_delete=models.CASCADE,
        related_name="reputation_logs",
    )
    change = models.FloatField()
    reason = models.CharField(max_length=255)
    
    def __str__(self):
        return f"{self.contributor.display_name}: {self.change} ({self.reason})"