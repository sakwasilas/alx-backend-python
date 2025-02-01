from django.test import TestCase
from django.contrib.auth.models import User
from messaging.models import Message, MessageHistory, Notification

class UserDeletionSignalTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='password')
        self.user2 = User.objects.create_user(username='user2', password='password')
        self.message = Message.objects.create(sender=self.user1, receiver=self.user2, content="Test Message")
        self.history = MessageHistory.objects.create(message=self.message, old_content="Old Content")
        self.notification = Notification.objects.create(user=self.user2, message=self.message, content="Test Notification")

    def test_user_deletion_cleans_up_data(self):
        self.user1.delete()  # Delete user1

        # Check if related data is deleted
        self.assertFalse(Message.objects.filter(sender=self.user1).exists())
        self.assertFalse(MessageHistory.objects.filter(message=self.message).exists())
        self.assertFalse(Notification.objects.filter(user=self.user1).exists())
