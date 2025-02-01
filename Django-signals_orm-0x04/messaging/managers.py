from django.db import models

class UnreadMessagesManager(models.Manager):
    def unread_for_user(self, user):
        """
        Retrieve unread messages for a specific user, optimized with .only().
        """
        return self.filter(receiver=user, read=False).only('id', 'sender', 'content', 'timestamp')
