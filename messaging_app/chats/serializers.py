from rest_framework import serializers
from .models import User, Message, Conversation

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'first_name', 'last_name', 'email', 'phone_number', 'role', 'created_at']

# Message Serializer
class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)  # Nested User serializer for the sender

    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'message_body', 'sent_at']

# Conversation Serializer
class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)  # Nested list of User objects
    messages = MessageSerializer(many=True, read_only=True)  # Nested list of Message objects

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'messages', 'created_at']