from django.db import models
from django.conf import settings
from apps.common.models import TimeStampedModel

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

    def adjust_reputation(self, change: float, reason: str) -> None:
        """
        Adjust contributor reputation and record an audit log.
        """
        self.reputation_score = max(0.0, self.reputation_score + change)
        self.save(update_fields=["reputation_score"])

        ReputationLog.objects.create(
            contributor=self,
            change=change,
            reason=reason,
        )