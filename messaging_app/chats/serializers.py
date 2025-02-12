from rest_framework import serializers
from .models import User, Conversation, Message

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['user_id', 'username', 'email', 'phone_number', 'role', 'full_name']

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

# Message Serializer
class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    message_body = serializers.CharField(max_length=1000)

    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'conversation', 'message_body', 'sent_at']

    def validate_message_body(self, value):
        if len(value.strip()) == 0:
            raise serializers.ValidationError("Message body cannot be empty.")
        return value

# Conversation Serializer
class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True, source='messages_set')

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'messages', 'created_at']