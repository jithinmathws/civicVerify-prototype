from django.test import TestCase
from common.services.view_tracking import should_count_view
from common.tests.utils import create_user


class ViewTrackingTests(TestCase):
    def setUp(self):
        self.user = create_user()
        self.content = self.user  # dummy content

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