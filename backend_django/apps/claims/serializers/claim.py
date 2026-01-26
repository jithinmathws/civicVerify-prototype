from rest_framework import serializers
from apps.claims.models import Claim, ClaimTag
from apps.user_auth.serializers import UserPublicSerializer

class ClaimBaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Claim
        fields = ["title", "description", "is_public"]

class ClaimListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Claim
        fields = ["id", "title", "status", "created_at"]

class ClaimTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClaimTag
        fields = ["name"]

class ClaimCreateSerializer(serializers.ModelSerializer):
    created_by = UserPublicSerializer(read_only=True)
    # Use SlugRelatedField to convert ClaimTag objects into their 'name' string
    tags = serializers.SlugRelatedField(
        many=True,
        slug_field="name",
        queryset=ClaimTag.objects.all(),
        required=False
    )

    class Meta:
        model = Claim
        fields = ["title", "description", "is_public", "tags", "created_by"]
        read_only_fields = ["created_by"]

    def create(self, validated_data):
        # Pop tags (many-to-many) before creating the Claim
        tag_names = validated_data.pop("tags", [])
        # Set created_by from request
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            validated_data["created_by"] = request.user
        claim = Claim.objects.create(**validated_data)

        # Add tags to the claim
        for name in tag_names:
            tag, _ = ClaimTag.objects.get_or_create(name=name)
            claim.tags.add(tag)

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
        read_only_fields = [
            "id",
            "created_by",
            "created_at",
        ]
