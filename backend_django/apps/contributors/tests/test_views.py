from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .factories import create_contributor


class MyContributorProfileViewTests(APITestCase):

    def test_get_own_profile(self):
        contributor = create_contributor()
        self.client.force_authenticate(user=contributor.user)

        url = reverse("my-contributor-profile")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["display_name"], contributor.display_name)

    def test_cannot_access_without_auth(self):
        url = reverse("my-contributor-profile")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)