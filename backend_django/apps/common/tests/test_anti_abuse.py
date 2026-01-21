from django.test import TestCase
from django.utils import timezone
from datetime import timedelta

from common.models import ContentView
from common.services.anti_abuse import is_rate_limited
from common.tests.utils import create_user


class AntiAbuseTests(TestCase):
    def setUp(self):
        self.user = create_user()
        self.content = self.user

    def test_rate_limit_triggered(self):
        for _ in range(31):
            ContentView.objects.create(
                content_object=self.content,
                user=self.user,
                viewer_ip="127.0.0.1",
            )

        self.assertTrue(is_rate_limited(self.user, None))