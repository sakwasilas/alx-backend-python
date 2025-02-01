from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
    sender = models.ForeignKey(User, related_name="sent_messages", on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name="received_messages", on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)
    edited_at = models.DateTimeField(null=True, blank=True)
    edited_by = models.ForeignKey(User, null=True, blank=True, related_name="edited_messages", on_delete=models.SET_NULL)
    read = models.BooleanField(default=False)  # Field to track if a message has been read
    parent_message = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='replies',
        on_delete=models.CASCADE
    )

    # Assign the custom manager
    objects = models.Manager()  # Default manager
    unread_messages = UnreadMessagesManager()  # Custom manager

    def __str__(self):
        return f"Message from {self.sender} to {self.receiver} - {self.content[:20]}"

    @property
    def is_reply(self):
        return self.parent_message is not None

    def get_all_replies(self):
        replies = self.replies.all()
        all_replies = list(replies)
        for reply in replies:
            all_replies.extend(reply.get_all_replies())
        return all_replies

class MessageHistory(models.Model):
    message = models.ForeignKey(Message, related_name="history", on_delete=models.CASCADE)
    old_content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"History of message {self.message.id}"

class Notification(models.Model):
    user = models.ForeignKey(User, related_name="notifications", on_delete=models.CASCADE)
    message = models.ForeignKey(Message, related_name="notifications", on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user}"

class UnreadMessagesManager(models.Manager):
    def get_unread_messages(self, user):
        # Filter unread messages for the specific user and optimize the query
        return self.filter(receiver=user, read=False).only('id', 'sender', 'content', 'timestamp')
