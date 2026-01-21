from typing import Any, Optional
from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _

from django.utils import timezone

from .base import TimeStampedModel

User = settings.AUTH_USER_MODEL

class ContentView(TimeStampedModel):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.UUIDField()
    content_object = GenericForeignKey("content_type", "object_id")

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="content_views",
    )

    viewer_ip = models.GenericIPAddressField(null=True, blank=True)

    last_viewed = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Content View")
        verbose_name_plural = _("Content Views")
        constraints = [
            models.UniqueConstraint(
                fields=["content_type", "object_id", "user", "viewer_ip"],
                name="unique_content_view_per_user_or_ip",
            )
        ]

    def __str__(self) -> str:
        viewer = getattr(self.user, "full_name", None) if self.user else None
        viewer = viewer or "Anonymous"
        return f"{self.content_type} viewed by {viewer}"

    @classmethod
    def record_view(
        cls,
        content_object: Any,
        user: Optional[User],
        viewer_ip: Optional[str],
    ) -> None:
        content_type = ContentType.objects.get_for_model(content_object)

        lookup = {
            "content_type": content_type,
            "object_id": content_object.id,
            "user": user,
            "viewer_ip": viewer_ip,
        }

        cls.objects.update_or_create(
            **lookup,
            defaults={"last_viewed": timezone.now()},
        )