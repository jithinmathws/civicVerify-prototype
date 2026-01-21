from django.test import TestCase
from django.utils import timezone
from datetime import timedelta

from apps.common.models import ContentView
from apps.common.services.anti_abuse import is_rate_limited
from apps.common.tests.utils import create_user


class AntiAbuseTests(TestCase):
    def setUp(self):
        self.user = create_user()
        self.content = self.user

    def test_rate_limit_triggered(self):
        # Same user generating many views from different IPs
        for _ in range(31):
            ContentView.objects.create(
                content_object=self.content,
                user=self.user,
                viewer_ip=f"127.0.0.{_ + 1}",
            )

        self.assertTrue(is_rate_limited(self.user, None))

    def test_rate_limit_not_triggered_under_threshold(self):
        # Same user generating views from different IPs
        for i in range(10):
            ContentView.objects.create(
                content_object=self.content,
                user=self.user,
                viewer_ip=f"127.0.0.{i + 1}",
            )

        self.assertFalse(is_rate_limited(self.user, None))