from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.contributors.tests.factories import create_user, create_contributor

User = get_user_model()


class ContributorModelTests(TestCase):

    def test_create_contributor_profile(self):
        """Contributor profile should be created and linked to user."""
        user = create_user()
        contributor = create_contributor(user=user)

        self.assertEqual(contributor.user, user)
        self.assertEqual(contributor.display_name, "Owner123")
        self.assertEqual(contributor.bio, "Test bio")
        self.assertEqual(contributor.reputation_score, 0.0)
        self.assertTrue(contributor.is_active)

    def test_reputation_log_creation(self):
        """ReputationLog should record changes in contributor reputation."""
        contributor = create_contributor(display_name="RepTester")

        contributor.adjust_reputation(10, "High-quality evidence")
        contributor.refresh_from_db()

        self.assertEqual(contributor.reputation_score, 10.0)
        self.assertEqual(contributor.reputation_logs.count(), 1)

        log = contributor.reputation_logs.first()
        self.assertEqual(log.change, 10)
        self.assertEqual(log.reason, "High-quality evidence")

    def test_multiple_reputation_changes(self):
        """Contributor reputation should accumulate across multiple logs."""
        contributor = create_contributor(display_name="MultiRep")

        contributor.adjust_reputation(5, "First contribution")
        contributor.adjust_reputation(-2, "Rejected evidence")
        contributor.refresh_from_db()

        self.assertEqual(contributor.reputation_score, 3.0)
        self.assertEqual(contributor.reputation_logs.count(), 2)

        reasons = set(
            contributor.reputation_logs.values_list("reason", flat=True)
        )
        self.assertSetEqual(
            reasons,
            {"First contribution", "Rejected evidence"},
        )