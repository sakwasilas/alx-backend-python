from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.utils.timezone import now
from django.contrib.auth.models import User
from messaging.models import Message, Notification, MessageHistory

@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    if created:  # Only create a notification for new messages
        Notification.objects.create(user=instance.receiver, message=instance)

@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    if instance.pk:  # Check if this is an update, not a new message
        try:
            old_message = Message.objects.get(pk=instance.pk)
            if old_message.content != instance.content:
                # Log the old content in MessageHistory
                MessageHistory.objects.create(message=old_message, old_content=old_message.content)
                # Mark the message as edited and set edited fields
                instance.edited = True
                instance.edited_at = now()
                # Ensure the edited_by field is set by the user performing the edit
                # (This requires passing the editing user explicitly during the save call)
        except Message.DoesNotExist:
            pass  # The message does not exist, so it's a new instance

@receiver(post_delete, sender=User)
def clean_up_user_data(sender, instance, **kwargs):
    """Delete all related data when a user is deleted."""
    # Delete all messages sent or received by the user
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()

    # Delete message histories
    MessageHistory.objects.filter(message__sender=instance).delete()
    MessageHistory.objects.filter(message__receiver=instance).delete()

    # Delete notifications related to the user
    Notification.objects.filter(user=instance).delete()
