from django.test import TestCase
from common.models import ContentView
from common.queries.analytics import get_view_count
from common.tests.utils import create_user


class AnalyticsTests(TestCase):
    def setUp(self):
        self.user = create_user()
        self.content = self.user

    def test_view_count(self):
        ContentView.record_view(
            content_object=self.content,
            user=None,
            viewer_ip="127.0.0.1",
        )
        ContentView.record_view(
            content_object=self.content,
            user=None,
            viewer_ip="127.0.0.2",
        )

        count = get_view_count(self.content)
        self.assertEqual(count, 2)