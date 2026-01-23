from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from apps.claims.models import Claim, ClaimTag, ClaimStatus
from django.contrib.auth import get_user_model

User = get_user_model()


class ClaimViewTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="creator@example.com",
            password="testpass123"
        )
        self.claim = Claim.objects.create(
            title="Public Claim",
            description="Visible to all",
            created_by=self.user,
            is_public=True,
        )
        self.private_claim = Claim.objects.create(
            title="Private Claim",
            description="Hidden",
            created_by=self.user,
            is_public=False,
        )
        self.assertEqual(Claim.objects.count(), 3)

    def test_status_immutability(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("claims:claim-list")

        data = {
            "title": "Hacky Claim",
            "description": "Trying to cheat",
            "status": ClaimStatus.PUBLISHED,
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["status"], ClaimStatus.DRAFT)


    def test_update_is_public(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("claims:claim-detail", args=[self.claim.id])

        data = {"is_public": False}
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data["is_public"])

    def test_list_public_claims(self):
        url = reverse("claims:claim-list")  # adjust to your URL name
        response = self.client.get(url)

        titles = [c["title"] for c in response.data]
        self.assertIn("Public Claim", titles)
        self.assertNotIn("Private Claim", titles)

    def test_retrieve_public_claim(self):
        url = reverse("claims:claim-detail", args=[self.claim.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_private_claim_requires_authentication(self):
        url = reverse("claims:claim-detail", args=[self.private_claim.id])
        response = self.client.get(url)
        # unauthenticated user should not see private claim
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # authenticated owner should see it
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Private Claim")

    def test_create_claim_requires_authentication(self):
        url = reverse("claims:claim-list")

        response = self.client.post(url, {
            "title": "New Claim",
            "description": "Created via API"
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, {
            "title": "New Claim",
            "description": "Created via API"
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_claim_with_tags(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("claims:claim-list")
        data = {
            "title": "Tagged Claim",
            "description": "Has tags",
            "tags": ["Science", "AI"]
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        claim_id = response.data["id"]
        claim = Claim.objects.get(id=claim_id)
        tags = list(claim.tags.values_list("name", flat=True))
        self.assertCountEqual(tags, ["science", "ai"])

class ClaimViewSetTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="creator@example.com", password="testpass123"
        )
        self.other_user = User.objects.create_user(
            email="other@example.com", password="testpass456"
        )
        self.claim = Claim.objects.create(
            title="Public Claim",
            description="Visible to all",
            created_by=self.user,
            is_public=True,
        )
        self.private_claim = Claim.objects.create(
            title="Private Claim",
            description="Hidden",
            created_by=self.user,
            is_public=False,
        )

    def test_list_claims(self):
        url = reverse("claims:claim-list")  # router registered name
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [c["title"] for c in response.data]
        self.assertIn("Public Claim", titles)
        self.assertNotIn("Private Claim", titles)

    def test_retrieve_public_claim(self):
        url = reverse("claims:claim-detail", args=[self.claim.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Public Claim")

    def test_retrieve_private_claim_owner_vs_other(self):
        url = reverse("claims:claim-detail", args=[self.private_claim.id])

        # unauthenticated user → not found
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # authenticated owner → success
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # authenticated non-owner → not found
        self.client.force_authenticate(user=self.other_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_claim_requires_authentication(self):
        url = reverse("claims:claim-list")  # POST to list = create
        data = {"title": "New Claim", "description": "Created via ViewSet"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "New Claim")
        self.assertEqual(response.data["status"], ClaimStatus.DRAFT)

    def test_update_claim_owner_only(self):
        url = reverse("claims:claim-detail", args=[self.claim.id])
        data = {"title": "Updated Title"}
        # non-owner
        self.client.force_authenticate(user=self.other_user)
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # owner
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Updated Title")

    def test_delete_claim_owner_only(self):
        url = reverse("claims:claim-detail", args=[self.claim.id])
        # non-owner
        self.client.force_authenticate(user=self.other_user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # owner
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Claim.objects.filter(id=self.claim.id).exists())