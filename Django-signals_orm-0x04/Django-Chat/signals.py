from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from messaging.models import Message, MessageHistory, Notification

@receiver(post_delete, sender=User)
def clean_up_user_data(sender, instance, **kwargs):
    # Delete messages sent or received by the user
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()

    # Delete message history associated with the user
    MessageHistory.objects.filter(message__sender=instance).delete()
    MessageHistory.objects.filter(message__receiver=instance).delete()

    # Delete notifications for the user
    Notification.objects.filter(user=instance).delete()
