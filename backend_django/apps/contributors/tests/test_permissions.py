from django.test import TestCase
from rest_framework.test import APIRequestFactory
from apps.contributors.permissions import IsContributorOwner
from .factories import create_contributor


class ContributorPermissionTests(TestCase):

    def test_owner_permission_allows_owner(self):
        contributor = create_contributor()
        request = APIRequestFactory().get("/")
        request.user = contributor.user

        permission = IsContributorOwner()
        self.assertTrue(
            permission.has_object_permission(request, None, contributor)
        )

    def test_owner_permission_denies_other_user(self):
        contributor = create_contributor()
        other = create_contributor()

        request = APIRequestFactory().get("/")
        request.user = other.user

        permission = IsContributorOwner()
        self.assertFalse(
            permission.has_object_permission(request, None, contributor)
        )