from django.test import TestCase
from apps.contributors.models import Contributor, ReputationLog
from .factories import create_contributor


class ContributorModelTests(TestCase):

    def test_adjust_reputation_creates_log(self):
        contributor = create_contributor()

        contributor.adjust_reputation(0.5, "Verified claim")

        contributor.refresh_from_db()
        self.assertEqual(contributor.reputation_score, 0.5)
        self.assertEqual(ReputationLog.objects.count(), 1)