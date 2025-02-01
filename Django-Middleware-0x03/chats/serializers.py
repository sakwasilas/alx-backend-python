from rest_framework import serializers
from .models import User, Conversation, Message


# User Serializer
class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()  # Combines first_name and last_name

    class Meta:
        model = User
        fields = ['user_id', 'first_name', 'last_name', 'full_name', 'email', 'phone_number', 'role', 'created_at']
        read_only_fields = ['user_id', 'created_at']

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"


# Message Serializer
class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.CharField(source='sender.email', read_only=True)  # Sender's email instead of nested object

    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'message_body', 'sent_at']
        read_only_fields = ['message_id', 'sent_at']

    def validate_message_body(self, value):
        if len(value) < 1:
            raise serializers.ValidationError("Message body cannot be empty.")
        return value


# Conversation Serializer
class ConversationSerializer(serializers.ModelSerializer):
    participants = serializers.SerializerMethodField()  # Custom handling of participants
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'messages', 'created_at']
        read_only_fields = ['conversation_id', 'created_at']

    def get_participants(self, obj):
        # Return participants as a list of email addresses
        return [user.email for user in obj.participants.all()]
