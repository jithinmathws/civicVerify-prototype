import uuid

from django.test import TestCase
from apps.common.services.view_tracking import should_count_view
from apps.common.tests.utils import create_user

class DummyContent:
    def __init__(self, created_by_id=None):
        self.id = uuid.uuid4()
        self.created_by_id = created_by_id

class ViewTrackingTests(TestCase):
    def setUp(self):
        self.user = create_user()
        self.content = DummyContent(created_by_id=self.user.id)

    def test_does_not_count_self_view(self):
        result = should_count_view(
            content_object=self.content,
            user=self.user,
            viewer_ip="127.0.0.1",
        )
        self.assertFalse(result)

    def test_requires_user_or_ip(self):
        result = should_count_view(
            content_object=self.content,
            user=None,
            viewer_ip=None,
        )
        self.assertFalse(result)

    def test_counts_valid_view(self):
        result = should_count_view(
            content_object=self.content,
            user=None,
            viewer_ip="127.0.0.1",
        )
        self.assertTrue(result)