from django.urls import path
from .views import *

urlpatterns = [
    path('me/', MyContributorProfileView.as_view(), name='my-contributor-profile'),
    path('<int:pk>/', PublicContributorDetailView.as_view(), name='public-contributor-detail'),
    path('reputation/', MyContributorReputationView.as_view(), name='my-contributor-reputation'),
]