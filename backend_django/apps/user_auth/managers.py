import uuid

from django.contrib.auth.models import UserManager as DjangoUserManager
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _


def generate_username() -> str:
    return f"user_{uuid.uuid4().hex[:10]}"


def validate_email_address(email: str) -> None:
    validate_email(email)


class UserManager(DjangoUserManager):
    def _create_user(self, email: str, password: str, **extra_fields):
        if not email:
            raise ValueError(_("An email address must be provided."))

        email = self.normalize_email(email)
        validate_email_address(email)

        user = self.model(
            email=email,
            username=generate_username(),
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email: str, password: str | None = None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email: str, password: str | None = None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if not extra_fields.get("is_staff"):
            raise ValueError(_("Superuser must have is_staff=True."))
        if not extra_fields.get("is_superuser"):
            raise ValueError(_("Superuser must have is_superuser=True."))

        return self._create_user(email, password, **extra_fields)