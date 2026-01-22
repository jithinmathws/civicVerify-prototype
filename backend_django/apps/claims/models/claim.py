import uuid
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.models import TimeStampedModel


class ClaimStatus(models.TextChoices):
    DRAFT = "draft", _("Draft")
    OPEN = "open", _("Open for Evidence")
    UNDER_REVIEW = "under_review", _("Under Review")
    VERIFIED = "verified", _("Verified")
    REJECTED = "rejected", _("Rejected")


class Claim(TimeStampedModel):
    """
    A verifiable assertion about a real-world event or media.
    """
    title = models.CharField(max_length=255)
    description = models.TextField()

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="claims_created",
        db_index=True,
    )

    status = models.CharField(
        max_length=20,
        choices=ClaimStatus.choices,
        default=ClaimStatus.DRAFT,
    )

    is_public = models.BooleanField(default=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["is_public"]),
        ]

    def __str__(self):
        return self.title or f"Claim {self.id}"

class ClaimTag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    claims = models.ManyToManyField(Claim, related_name="tags")
    
    def __str__(self):
        return self.name