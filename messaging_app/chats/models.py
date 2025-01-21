import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models


# Custom User Model
class User(AbstractUser):
    user_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

    def __str__(self):
        return self.username


# Conversation Model
class Conversation(models.Model):
    # Adding custom conversation_id (UUID) field for unique conversation identifiers
    conversation_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    participants = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Conversation {self.conversation_id} ({', '.join([user.username for user in self.participants.all()])})"


# Message Model
class Message(models.Model):
    # Adding custom fields for message_id, message_body, and sent_at
    message_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)  # Unique message identifier
    message_body = models.TextField()  # The body of the message (content)
    sent_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the message was sent
    
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')

    def __str__(self):
        return f"Message {self.message_id} from {self.sender.username} in Conversation {self.conversation.conversation_id}"
