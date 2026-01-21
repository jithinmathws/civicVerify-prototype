import uuid
from django.contrib.auth import get_user_model

User = get_user_model()

def create_user(email="test@example.com", **kwargs):
    defaults = {
        "password": "testpass123",
        "full_name": "User",
    }
    defaults.update(kwargs)
    return User.objects.create_user(email=email, **defaults)