import uuid
from django.contrib.auth import get_user_model

User = get_user_model()

def create_user(email="test@example.com", **kwargs):
    defaults = {
        "password": "testpass123",
        "first_name": "Test",
        "last_name": "User",
        "id_no": uuid.uuid4().int >> 64,
    }
    defaults.update(kwargs)
    return User.objects.create_user(email=email, **defaults)