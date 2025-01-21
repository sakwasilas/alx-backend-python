import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models


# Custom User Model
class User(AbstractUser):
    # Custom primary key (optional)
    user_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    
    # Defining fields from AbstractUser explicitly
    email = models.EmailField(unique=True)  # Email is already in AbstractUser but explicitly defined
    first_name = models.CharField(max_length=30)  # Explicitly adding first_name
    last_name = models.CharField(max_length=30)  # Explicitly adding last_name
    password = models.CharField(max_length=128)  # Explicitly adding password, though AbstractUser already handles this
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
