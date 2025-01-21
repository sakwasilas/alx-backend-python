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
    phone_number=models.CharField(max_length=12)
    password = models.CharField(max_length=128)  # Explicitly adding password, though AbstractUser already handles this
    def __str__(self):
        return self.username

        # Enum field for role
    ROLE_CHOICES = [
        ('guest', 'Guest'),
        ('host', 'Host'),
        ('admin', 'Admin'),
    ]


# Conversation Model
class Conversation(models.Model):
    # Fields
    conversation_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    participants_id = models.UUIDField()  # No many-to-many, just a UUID to indicate participants
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['conversation_id']),  # Index on conversation_id for quick lookups
        ]
    
    def __str__(self):
        return f"Conversation {self.conversation_id} created at {self.created_at}"

# Message Model
class Message(models.Model):
    # Fields
    message_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    sender_id = models.UUIDField()  # No foreign key, just a UUID to indicate the sender
    message_body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['sender_id']),  # Index on sender_id for quicker lookups
        ]
    
    def __str__(self):
        return f"Message from {self.sender_id} at {self.sent_at}"


