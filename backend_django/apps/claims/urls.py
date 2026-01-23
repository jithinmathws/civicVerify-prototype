from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.claims.views.claim_viewset import ClaimViewSet

app_name = "claims"

router = DefaultRouter()
router.register(r"claims", ClaimViewSet, basename="claim")

urlpatterns = [
    path("", include(router.urls)),
]