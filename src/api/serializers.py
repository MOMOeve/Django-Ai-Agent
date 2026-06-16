from rest_framework import serializers

from documents.models import Document


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class ChatSerializer(serializers.Serializer):
    message = serializers.CharField()
    thread_id = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    agent_type = serializers.ChoiceField(
        choices=["document", "movie", "supervisor"],
        default="supervisor",
    )


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ["id", "title", "content", "created_at", "updated_at"]
