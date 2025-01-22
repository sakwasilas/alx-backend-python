from rest_framework import viewsets
from rest_framework import filters
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend  # Import DjangoFilterBackend
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer

class ConversationViewSet(viewsets.ModelViewSet):
    """
    Viewset for listing and creating conversations.
    """
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)  # Enable filtering and ordering
    filterset_fields = ['participants']  # Example: filter conversations by participants
    ordering_fields = ['created_at']  # Allow ordering by 'created_at' field

    def create(self, request, *args, **kwargs):
        """
        Create a new conversation. Typically, this would involve specifying participants.
        """
        participants = request.data.get('participants', [])
        if len(participants) < 2:
            return Response({"error": "At least two participants are required."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create the conversation
        conversation = Conversation.objects.create()
        conversation.participants.set(participants)  # Set participants
        conversation.save()
        
        # Return the conversation's serialized data
        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class MessageViewSet(viewsets.ModelViewSet):
    """
    Viewset for listing and creating messages.
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)  # Enable filtering and ordering
    filterset_fields = ['conversation', 'sender_id']  # Example: filter messages by conversation or sender
    ordering_fields = ['sent_at']  # Allow ordering by 'sent_at' field

    def create(self, request, *args, **kwargs):
        """
        Create a new message in an existing conversation.
        """
        conversation_id = request.data.get('conversation_id')
        sender_id = request.data.get('sender_id')
        message_body = request.data.get('message_body')

        # Ensure the conversation exists
        try:
            conversation = Conversation.objects.get(conversation_id=conversation_id)
        except Conversation.DoesNotExist:
            return Response({"error": "Conversation not found."}, status=status.HTTP_404_NOT_FOUND)

        # Ensure sender is part of the conversation
        if sender_id not in conversation.participants.values_list('user_id', flat=True):
            return Response({"error": "Sender is not a participant in this conversation."}, status=status.HTTP_400_BAD_REQUEST)

        # Create the message
        message = Message.objects.create(
            conversation=conversation,
            sender_id=sender_id,
            message_body=message_body
        )
        message.save()

        # Return the serialized message data
        serializer = self.get_serializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)