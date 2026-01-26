from rest_framework import serializers
from apps.user_auth.models import User


class UserPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "full_name"]
        read_only_fields = ["id", "username", "email", "full_name"]

__all__ = ["UserPublicSerializer"]