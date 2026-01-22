from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from apps.user_auth.models import User
from apps.contributors.signals import create_contributor_profile  # your signal handler
from apps.contributors.tests.factories import create_user
from apps.contributors.models import Contributor

User = get_user_model()


class ContributorSignalTests(TestCase):

    def test_contributor_profile_created_on_user_creation(self):
        """
        Contributor profile should be automatically created
        when a user is created.
        """
        user = create_user(email="owner@example.com")

        # Check if contributor profile was created
        self.assertTrue(
            Contributor.objects.filter(user=user).exists()
        )

        contributor = Contributor.objects.get(user=user)

        self.assertEqual(Contributor.objects.filter(user=user).count(), 1) # Should only have 1 contributor profile
        self.assertEqual(contributor.user, user)
        self.assertEqual(contributor.reputation_score, 0.0)
        self.assertTrue(contributor.is_active)

    def test_contributor_not_duplicated_on_user_save(self):
        user = create_user(email="owner@example.com")

        # Saving user again should not create a second contributor
        user.save()

        self.assertEqual(
            Contributor.objects.filter(user=user).count(),
            1
        ) # Should still only have 1 contributor profile


class ContributorSignalNegativeTests(TestCase):

    def test_no_contributor_created_when_signal_disconnected(self):
        post_save.disconnect(create_contributor_profile, sender=User)

        try:
            user = create_user(email="nosignal@example.com")

            self.assertFalse(
                Contributor.objects.filter(user=user).exists(),
                "Contributor should not be created when signal is disconnected"
            )
        finally:
            # Always reconnect signal
            post_save.connect(create_contributor_profile, sender=User)