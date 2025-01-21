
from rest_framework import serializers
from .models import User, Message, Conversation
from rest_framework.exceptions import ValidationError


# User Serializer
class UserSerializer(serializers.ModelSerializer):
    # Custom field for full name (using SerializerMethodField)
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['user_id', 'first_name', 'last_name', 'email', 'phone_number', 'role', 'created_at', 'full_name']

    def get_full_name(self, obj):
        # Combine first_name and last_name to return full name
        return f"{obj.first_name} {obj.last_name}"

    # Custom validation for email field
    def validate_email(self, value):
        if "example" in value:
            raise ValidationError("Email cannot contain 'example'.")
        return value


# Message Serializer
class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)  # Nested User serializer for the sender
    message_body = serializers.CharField(max_length=500)  # Using CharField for the message body
    
    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'message_body', 'sent_at']

    # Custom validation for message body
    def validate_message_body(self, value):
        if not value.strip():
            raise ValidationError("Message body cannot be empty.")
        return value


# Conversation Serializer
class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)  # Nested list of User objects (many participants)
    messages = MessageSerializer(many=True, read_only=True)  # Nested list of Message objects
    conversation_name = serializers.CharField(source='get_conversation_name', read_only=True)  # Using CharField for custom field

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'messages', 'created_at', 'conversation_name']

    # Custom method to get the conversation name (using SerializerMethodField)
    def get_conversation_name(self, obj):
        # Return a formatted string for the conversation name
        return f"Conversation {obj.conversation_id}"