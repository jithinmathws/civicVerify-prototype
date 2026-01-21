from typing import Any, Optional

def should_count_view(
    content_object: Any,
    user: Optional[Any],
    viewer_ip: Optional[str],
) -> bool:
    # 1. Do not count self-views
    content_owner_id = getattr(content_object, "created_by_id", None)

    if user:
        if getattr(content_object, "pk", None) == getattr(user, "pk", None):
            return False

        if content_owner_id == user.id:
            return False

        if getattr(user, "is_locked_out", False):
            return False

    # 2. Anonymous views must have IP
    if not user and not viewer_ip:
        return False

    # 3. Rate limiting / abuse checks
    from apps.common.services.anti_abuse import is_rate_limited

    if is_rate_limited(user, viewer_ip):
        return False

    return True