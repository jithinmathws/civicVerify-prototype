import uuid

from django.contrib.auth import get_user_model
from apps.contributors.models import Contributor

User = get_user_model()


def create_user(**kwargs):
    defaults = {
        "email": f"test_{uuid.uuid4().hex[:6]}@example.com",
        "password": "testpass123",
        "full_name": "Test User",
    }
    defaults.update(kwargs)
    return User.objects.create_user(**defaults)


def create_contributor(user=None, **kwargs):
    if not user:
        user = create_user()

    contributor = user.contributor_profile  # 👈 already exists
    
    # Set default values if not provided
    if 'display_name' not in kwargs:
        kwargs['display_name'] = "Owner123"
    if 'bio' not in kwargs:
        kwargs['bio'] = "Test bio"

    for key, value in kwargs.items():
        setattr(contributor, key, value)

    contributor.save()
    return contributor