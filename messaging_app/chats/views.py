from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from django_filters import rest_framework as filters

# ViewSet for Conversation
class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    filter_backends = (filters.DjangoFilterBackend,)  # Added filter backend for filtering
    filterset_fields = ['participants']  # Allow filtering by participants

    def list(self, request, *args, **kwargs):
        """
        Override the list method to include filtering.
        """
        return super().list(request, *args, **kwargs)

# ViewSet for Message
class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    filter_backends = (filters.DjangoFilterBackend,)  # Added filter backend for filtering
    filterset_fields = ['conversation', 'sender']  # Allow filtering by conversation and sender

    @action(detail=True, methods=['post'])
    def send_message(self, request, *args, **kwargs):
        """
        Custom action to send a message to a conversation.
        """
        conversation = self.get_object()  # Get the conversation from the URL
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Set the sender to the current user and associate the message with the conversation
            serializer.save(sender=request.user, conversation=conversation)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)