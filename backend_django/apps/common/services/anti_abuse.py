from datetime import timedelta

def is_rate_limited(user, viewer_ip) -> bool:
    from apps.common.models.content_view import ContentView
    from django.utils import timezone

    cutoff = timezone.now() - timedelta(hours=1)

    qs = ContentView.objects.filter(created_at__gte=cutoff)

    if user:
        qs = qs.filter(user=user)
    elif viewer_ip:
        qs = qs.filter(viewer_ip=viewer_ip)
    else:
        return True

    return qs.count() > 30