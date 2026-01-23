from django.test import TestCase
from django.db.utils import IntegrityError
from django.contrib.auth import get_user_model

from apps.claims.models.claim import Claim, ClaimTag, ClaimStatus

User = get_user_model()


class ClaimModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="creator@example.com",
            password="testpass123"
        )

    def test_create_claim(self):
        """Claim should be created with correct defaults."""
        claim = Claim.objects.create(
            title="Test Claim",
            description="This is a test claim.",
            created_by=self.user,
        )

        self.assertEqual(claim.title, "Test Claim")
        self.assertEqual(claim.description, "This is a test claim.")
        self.assertEqual(claim.created_by, self.user)
        self.assertEqual(claim.status, ClaimStatus.DRAFT)
        self.assertTrue(claim.is_public)
        self.assertIsNotNone(claim.created_at)
        self.assertIsNotNone(claim.updated_at)

    def test_claim_string_representation(self):
        claim = Claim.objects.create(
            title="Readable Title",
            description="Test",
            created_by=self.user,
        )
        self.assertEqual(str(claim), "Readable Title")

    def test_claim_string_fallback_when_title_missing(self):
        claim = Claim.objects.create(
            title="",
            description="No title claim",
            created_by=self.user,
        )
        self.assertTrue(str(claim).startswith("Claim "))

    def test_claim_ordering(self):
        """Claims should be ordered by newest first."""
        older = Claim.objects.create(
            title="Old Claim",
            description="Old",
            created_by=self.user,
        )

        newer = Claim.objects.create(
            title="New Claim",
            description="New",
            created_by=self.user,
        )

        claims = list(Claim.objects.order_by("-created_at"))
        self.assertEqual(claims[0], newer)
        self.assertEqual(claims[1], older)

    def test_private_claim(self):
        claim = Claim.objects.create(
            title="Private Claim",
            description="Hidden",
            created_by=self.user,
            is_public=False,
        )

        self.assertFalse(claim.is_public)
    
    def test_claim_without_created_by(self):
        claim = Claim.objects.create(title="No User", description="Anonymous")
        self.assertIsNone(claim.created_by)



class ClaimTagModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="tagger@example.com",
            password="testpass123"
        )

        self.claim = Claim.objects.create(
            title="Tagged Claim",
            description="Has tags",
            created_by=self.user,
        )

    def test_create_claim_tag(self):
        tag = ClaimTag.objects.create(name="Politics")
        self.assertEqual(str(tag), "Politics")

    def test_tag_uniqueness_case_insensitive(self):
        ClaimTag.objects.create(name="Science")

        with self.assertRaises(IntegrityError):
            ClaimTag.objects.create(name="science")

    def test_assign_tag_to_claim(self):
        tag = ClaimTag.objects.create(name="Health")
        self.claim.tags.add(tag)

        self.assertEqual(self.claim.tags.count(), 1)
        self.assertIn(tag, self.claim.tags.all())

    def test_claim_can_have_multiple_tags(self):
        tag1 = ClaimTag.objects.create(name="Tech")
        tag2 = ClaimTag.objects.create(name="AI")

        self.claim.tags.add(tag1, tag2)

        self.assertEqual(self.claim.tags.count(), 2)
        self.assertIn(self.claim, tag1.claim_set.all())
        self.assertIn(self.claim, tag2.claim_set.all())

    def test_tag_uniqueness_with_integrity_error(self):
        ClaimTag.objects.create(name="Science")

        with self.assertRaises(IntegrityError):
            ClaimTag.objects.create(name="Science")
