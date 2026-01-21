from typing import Any, Optional
from django.contrib.auth import get_user_model

User = get_user_model()

def should_count_view(content_object: Any, user: Optional[User], viewer_ip: Optional[str]) -> bool:
    if user and getattr(content_object, "created_by_id", None) == user.id:
        return False

    if user and user.is_locked_out:
        return False

    if not user and not viewer_ip:
        return False

    from apps.common.services.anti_abuse import is_rate_limited

    if is_rate_limited(user, viewer_ip):
        return False

    return True