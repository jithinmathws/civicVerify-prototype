from rest_framework import serializers
from apps.claims.models import Claim
from apps.users.serializers import UserPublicSerializer

class ClaimBaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Claim
        fields = ["title", "description", "is_public"]

class ClaimCreateSerializer(ClaimBaseSerializer):

    def create(self, validated_data):
        validated_data.pop("created_by", None)
        request = self.context.get("request")
        user = getattr(request, "user", None)

        return Claim.objects.create(
            created_by=user,
            **validated_data
        )

class ClaimDetailSerializer(ClaimBaseSerializer):
    created_by = UserPublicSerializer(read_only=True)
    
    class Meta(ClaimBaseSerializer.Meta):
        fields = ClaimBaseSerializer.Meta.fields + [
            "id",
            "status",
            "created_by",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "status",
            "created_by",
            "created_at",
        ]

class ClaimListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Claim
        fields = ["id", "title", "status", "created_at"]

class ClaimTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClaimTag
        fields = ["name"]

class ClaimCreateSerializer(serializers.ModelSerializer):
    tags = serializers.ListField(
        child=serializers.CharField(),
        required=False,
    )

    class Meta:
        model = Claim
        fields = ["title", "description", "is_public", "tags"]

    def create(self, validated_data):
        tags_data = validated_data.pop("tags", [])
        claim = Claim.objects.create(**validated_data)

        self._set_tags(claim, tags_data)
        return claim

    def _set_tags(self, claim, tags):
        normalized_tags = {
            tag.strip().lower()
            for tag in tags
            if tag.strip()
        }

        for tag_name in normalized_tags:
            tag, _ = ClaimTag.objects.get_or_create(name=tag_name)
            claim.tags.add(tag)

class ClaimUpdateSerializer(ClaimCreateSerializer):

    def update(self, instance, validated_data):
        tags_data = validated_data.pop("tags", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        if tags_data is not None:
            instance.tags.clear()
            self._set_tags(instance, tags_data)

        return instance

class ClaimDetailSerializer(serializers.ModelSerializer):
    tags = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="name"
    )
    created_by = UserPublicSerializer(read_only=True)

    class Meta:
        model = Claim
        fields = [
            "id",
            "title",
            "description",
            "status",
            "is_public",
            "created_by",
            "created_at",
            "tags",
        ]
