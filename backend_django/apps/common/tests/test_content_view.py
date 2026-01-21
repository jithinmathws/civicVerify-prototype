from django.test import TestCase
from django.contrib.contenttypes.models import ContentType

from common.models import ContentView
from common.tests.utils import create_user


class ContentViewTests(TestCase):
    def setUp(self):
        self.user = create_user()
        self.content = self.user  # using User as dummy content object

    def test_record_view_creates_entry(self):
        ContentView.record_view(
            content_object=self.content,
            user=self.user,
            viewer_ip="127.0.0.1",
        )

        self.assertEqual(ContentView.objects.count(), 1)

    def test_duplicate_view_updates_not_creates(self):
        ContentView.record_view(
            content_object=self.content,
            user=self.user,
            viewer_ip="127.0.0.1",
        )
        ContentView.record_view(
            content_object=self.content,
            user=self.user,
            viewer_ip="127.0.0.1",
        )

        self.assertEqual(ContentView.objects.count(), 1)