def get_view_count(content_object):
    from django.contrib.contenttypes.models import ContentType
    from apps.common.models.content_view import ContentView

    ct = ContentType.objects.get_for_model(content_object)
    return ContentView.objects.filter(
        content_type=ct,
        object_id=content_object.id,
    ).count()


def get_unique_viewers(content_object):
    from django.contrib.contenttypes.models import ContentType
    from apps.common.models.content_view import ContentView

    ct = ContentType.objects.get_for_model(content_object)
    return (
        ContentView.objects.filter(content_type=ct, object_id=content_object.id)
        .values("user", "viewer_ip")
        .distinct()
        .count()
    )