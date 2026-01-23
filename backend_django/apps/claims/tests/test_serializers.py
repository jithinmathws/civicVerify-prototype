from django.test import TestCase
from django.db.utils import IntegrityError
from django.contrib.auth import get_user_model

from apps.claims.models.claim import Claim, ClaimTag, ClaimStatus
from apps.claims.serializers.claim import *

User = get_user_model()


class ClaimCreateSerializerTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="creator@example.com",
            password="testpass123"
        )
    
    def test_claim_create_serializer_valid(self):
        serializer = ClaimCreateSerializer(
            data={
                "title": "Test Claim",
                "description": "Test description",
            }
        )

        self.assertTrue(serializer.is_valid())

    def test_created_by_is_ignored_in_payload(self):
        serializer = ClaimCreateSerializer(
            data={
                "title": "Test",
                "description": "Test",
                "created_by": 999,
            }
        )
        serializer.is_valid()
        self.assertNotIn("created_by", serializer.validated_data)


    def test_created_by_is_read_only(self):
        serializer = ClaimCreateSerializer(
            data={
                "title": "Test",
                "description": "Test",
                "created_by": self.user.id,
            }
        )

        serializer.is_valid()
        self.assertNotIn("created_by", serializer.validated_data)

    def test_tags_are_normalized(self):
        serializer = ClaimCreateSerializer(
            data={
                "title": "Test",
                "description": "Test",
                "tags": ["Science", " science ", "AI", "ai"],
            }
        )

        serializer.is_valid(raise_exception=True)
        claim = serializer.save(created_by=self.user)

        tags = list(claim.tags.values_list("name", flat=True))
        self.assertCountEqual(tags, ["science", "ai"])

    def test_empty_tags_are_ignored(self):
        serializer = ClaimCreateSerializer(
            data={
                "title": "Test",
                "description": "Test",
                "tags": ["", "   ", "Science"],
            }
        )

        serializer.is_valid(raise_exception=True)
        claim = serializer.save(created_by=self.user)

        tags = list(claim.tags.values_list("name", flat=True))
        self.assertEqual(tags, ["science"])

    def test_duplicate_tags_in_payload(self):
        serializer = ClaimCreateSerializer(
            data={
                "title": "Test",
                "description": "Test",
                "tags": ["science", "Science", "SCIENCE"],
            }
        )

        serializer.is_valid(raise_exception=True)
        claim = serializer.save(created_by=self.user)

        self.assertEqual(claim.tags.count(), 1)

    def test_existing_tag_is_reused(self):
        existing = ClaimTag.objects.create(name="science")

        serializer = ClaimCreateSerializer(
            data={
                "title": "Test",
                "description": "Test",
                "tags": ["Science"],
            }
        )

        serializer.is_valid(raise_exception=True)
        claim = serializer.save(created_by=self.user)

        self.assertEqual(ClaimTag.objects.filter(name="science").count(), 1)
        self.assertIn(existing, claim.tags.all())
    
    def test_tags_must_be_list(self):
        serializer = ClaimCreateSerializer(
            data={
                "title": "Test",
                "description": "Test",
                "tags": "science",
            }
        )
        self.assertFalse(serializer.is_valid())


class ClaimDetailSerializerTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="testuser@example.com",
            password="testpass"
        )
        self.claim = Claim.objects.create(
            title="Test Claim",
            description="Test Description",
            created_by=self.user,
        )
        self.serializer = ClaimDetailSerializer(self.claim)

    def test_claim_detail_serializer_outputs_tags(self):
        claim = Claim.objects.create(
            title="Test",
            description="Test",
            created_by=self.user,
        )

        tag = ClaimTag.objects.create(name="science")
        claim.tags.add(tag)

        serializer = ClaimDetailSerializer(claim)
        self.assertEqual(serializer.data["tags"], ["science"])

    def test_claim_detail_completeness(self):
        data = self.serializer.data
        self.assertEqual(data["title"], "Test Claim")
        self.assertEqual(data["description"], "Test Description")
        self.assertEqual(data["status"], ClaimStatus.DRAFT)
        self.assertEqual(data["created_by"]["id"], self.user.id)

    def test_invalid_payload(self):
        data = {"description": "Missing title"}
        serializer = ClaimCreateSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("title", serializer.errors)

    def test_public_private_flag(self):
        claim = Claim.objects.create(
            title="Test",
            description="Test",
            created_by=self.user,
            is_public=True,
        )
        data = ClaimDetailSerializer(claim).data
        self.assertTrue(data["is_public"])
    
    def test_claim_with_multiple_tags_serialization(self):
        claim = Claim.objects.create(
            title="Test Claim",
            description="Test Description",
            created_by=self.user,
        )

        tags = [
            ClaimTag.objects.create(name="science"),
            ClaimTag.objects.create(name="ai"),
            ClaimTag.objects.create(name="technology"),
        ]

        claim.tags.add(*tags)

        serializer = ClaimDetailSerializer(claim)
        self.assertCountEqual(
            serializer.data["tags"],
            ["science", "ai", "technology"]
        )

