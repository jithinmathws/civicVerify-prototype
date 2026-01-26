from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model

from apps.claims.models.claim import Claim
from apps.contributors.models import Contributor

User = get_user_model()

class BasicTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="order@example.com", password="pass123"
        )

        self.old = Claim.objects.create(
            title="Old",
            description="Old",
            created_by=self.user,
            is_public=True,
        )

        self.new = Claim.objects.create(
            title="Public",
            description="New",
            created_by=self.user,
            is_public=True,
        )

    def test_list_claims_ordering(self):
        url = reverse("claims:claim-list")
        response = self.client.get(url)
        
        # 1. Ensure the request was successful (200 OK)
        self.assertEqual(response.status_code, 200)

        # 2. Handle Pagination: Check if data is in 'results' or the root
        if isinstance(response.data, dict) and "results" in response.data:
            data = response.data["results"]
        else:
            data = response.data

        # 3. Extract titles (safely using .get to avoid further KeyErrors)
        titles = [c.get("title") if isinstance(c, dict) else c for c in data]
        
        # 4. Assertions
        self.assertTrue(len(titles) > 0, "The claims list is empty.")
        self.assertEqual(titles[0], "Public")


class ClaimAnonymousPermissionTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="owner@example.com", password="pass123"
        )

        self.public_claim = Claim.objects.create(
            title="Public",
            description="Visible",
            created_by=self.user,
            is_public=True,
        )

        self.private_claim = Claim.objects.create(
            title="Private",
            description="Hidden",
            created_by=self.user,
            is_public=False,
        )

    def test_anonymous_can_list_public_claims(self):
        url = reverse("claims:claim-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_anonymous_can_retrieve_public_claim(self):
        url = reverse("claims:claim-detail", args=[self.public_claim.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_anonymous_cannot_retrieve_private_claim(self):
        url = reverse("claims:claim-detail", args=[self.private_claim.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_anonymous_cannot_create_claim(self):
        url = reverse("claims:claim-list")
        response = self.client.post(url, {
            "title": "Nope",
            "description": "No auth",
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class ClaimAuthenticatedNonOwnerPermissionTests(APITestCase):
    def setUp(self):
        self.client = APIClient()

        self.owner = User.objects.create_user(
            email="owner@example.com", password="pass123"
        )
        self.other_user = User.objects.create_user(
            email="other@example.com", password="pass456"
        )

        self.public_claim = Claim.objects.create(
            title="Public",
            description="Visible",
            created_by=self.owner,
            is_public=True,
        )

        self.private_claim = Claim.objects.create(
            title="Private",
            description="Hidden",
            created_by=self.owner,
            is_public=False,
        )

        self.client.force_authenticate(user=self.other_user)

    def test_authenticated_user_can_view_public_claim(self):
        url = reverse("claims:claim-detail", args=[self.public_claim.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_authenticated_user_cannot_view_private_claim_of_others(self):
        url = reverse("claims:claim-detail", args=[self.private_claim.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_authenticated_user_cannot_update_claim(self):
        url = reverse("claims:claim-detail", args=[self.public_claim.id])
        response = self.client.patch(url, {"title": "Hack"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_user_cannot_delete_claim(self):
        url = reverse("claims:claim-detail", args=[self.public_claim.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class ClaimContributorPermissionTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="contrib@example.com", password="pass123"
        )

        # contributor profile is auto-created by signal; ensure it exists
        contributor = getattr(self.user, "contributor_profile", None)
        if not contributor:
            Contributor.objects.create(
                user=self.user,
                display_name="Contributor",
            )

        self.client.force_authenticate(user=self.user)

    def test_contributor_can_create_claim(self):
        url = reverse("claims:claim-list")
        self.client.force_authenticate(user=self.user)  # ensure contributor is logged in
        response = self.client.post(url, {
            "title": "New Claim",
            "description": "Allowed",
        }, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "New Claim")
        self.assertEqual(response.data["description"], "Allowed")
        self.assertEqual(response.data["created_by"]["id"], self.user.id)
        self.assertEqual(response.data["status"], ClaimStatus.DRAFT)

        self.assertTrue(
            Claim.objects.filter(title="New Claim", created_by=self.user).exists()
        )

class ClaimOwnerPermissionTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.owner = User.objects.create_user(
            email="owner@example.com", password="pass123"
        )

        self.claim = Claim.objects.create(
            title="Mine",
            description="Owned",
            created_by=self.owner,
            is_public=False,
        )

        self.client.force_authenticate(user=self.owner)

    def test_owner_can_view_private_claim(self):
        url = reverse("claims:claim-detail", args=[self.claim.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_owner_can_update_claim(self):
        url = reverse("claims:claim-detail", args=[self.claim.id])
        response = self.client.patch(url, {"title": "Updated"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_owner_can_delete_claim(self):
        url = reverse("claims:claim-detail", args=[self.claim.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_admin_can_delete_any_claim(self):
        admin = User.objects.create_superuser(
            email="admin@test.com", password="pass123"
        )
        self.client.force_authenticate(user=admin)

        url = reverse("claims:claim-detail", args=[self.claim.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

