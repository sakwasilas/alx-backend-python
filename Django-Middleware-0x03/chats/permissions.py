
from rest_framework import permissions
from .models import Conversation

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to allow only participants of a conversation to send, view, update, or delete messages.
    """

    def has_permission(self, request, view):
        """
        Check if the user is authenticated and a participant in the conversation.
        """
        # Allow access only to authenticated users
        if not request.user.is_authenticated:
            return False

        # Allow access to certain views like creating messages (POST)
        if request.method == 'POST':
            return True

        # For other methods (GET, PUT, DELETE), check if the user is a participant
        conversation_id = view.kwargs.get('conversation_id')  # Assuming URL is /conversations/{conversation_id}/messages/
        try:
            conversation = Conversation.objects.get(conversation_id=conversation_id)
            if request.user in conversation.participants.all():
                return True
            else:
                return False
        except Conversation.DoesNotExist:
            return False

    def has_object_permission(self, request, view, obj):
        """
        Check if the user is a participant in the specific conversation object for actions like update and delete.
        """
        # For Message object, ensure the user is a participant in the conversation.
        conversation = obj.conversation  # Assuming Message model has a ForeignKey to Conversation
        return request.user in conversation.participants.all()
