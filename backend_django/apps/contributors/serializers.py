from rest_framework import serializers
from .models import Contributor, ReputationLog


class ContributorSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributor
        fields = [
            "id",
            "display_name",
            "bio",
            "reputation_score",
            "is_active",
            "created_at",
        ]
        read_only_fields = ["id", "reputation_score", "is_active", "created_at"]

class ContributorPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributor
        fields = [
            "id",
            "display_name",
            "bio",
            "reputation_score",
        ]

class ContributorSelfSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributor
        fields = [
            "id",
            "display_name",
            "bio",
            "reputation_score",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "reputation_score",
            "is_active",
            "created_at",
            "updated_at",
        ]


class ContributorUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributor
        fields = ["display_name", "bio"]


class ReputationLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReputationLog
        fields = [
            "id",
            "change",
            "reason",
            "created_at",
        ]
        read_only_fields = fields
