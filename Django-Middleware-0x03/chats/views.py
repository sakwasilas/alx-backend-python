from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from django.shortcuts import get_object_or_404

from .permissions import IsParticipantOfConversation
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User  # To validate participants

from django_filters.rest_framework import DjangoFilterBackend
from .filters import MessageFilter  # Import the filter class

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['participants__email', 'participants__first_name', 'participants__last_name']
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]  # Enforce participant check for all actions


    @action(detail=False, methods=['post'], url_path='create', url_name='create_conversation')
    def create_conversation(self, request):
        participants_data = request.data.get('participants', [])
        if not participants_data:
            return Response(
                {"error": "Participants list cannot be empty."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validate that the participants are valid users
        participants = []
        for email in participants_data:
            try:
                user = User.objects.get(email=email)
                participants.append(user.id)  # Appending user id instead of full user object
            except User.DoesNotExist:
                return Response(
                    {"error": f"User with email {email} not found."},
                    status=status.HTTP_400_BAD_REQUEST
                )

        # Create the conversation with the validated participants
        conversation = Conversation.objects.create()
        conversation.participants.set(participants)
        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


    def get_queryset(self):
        # Allow users to see only their conversations
        user = self.request.user
        return Conversation.objects.filter(participants=user)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['message_body', 'sender__email']
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]  # Enforce participant check for all actions

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]  # Enable filtering and ordering
    filterset_class = MessageFilter  # Apply the MessageFilter class
    ordering_fields = ['created_at']  # Allow ordering messages by creation date
    ordering = ['created_at']  # Default ordering is by creation date

    def create(self, request, *args, **kwargs):
        conversation_id = request.data.get('conversation_id')
        message_body = request.data.get('message_body')
        sender = request.user

        if not conversation_id or not message_body:
            return Response(
                {"error": "conversation_id and message_body are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        conversation = get_object_or_404(Conversation, pk=conversation_id)

        # Ensure the sender is a participant of the conversation
        if sender not in conversation.participants.all():
            return Response(
                {"error": "You are not a participant in this conversation."},
                status=status.HTTP_403_FORBIDDEN
            )

        message = Message.objects.create(conversation=conversation, sender=sender, message_body=message_body)
        serializer = self.get_serializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


    def get_queryset(self):
        user = self.request.user
        # Allow users to see only messages in conversations they are part of
        return Message.objects.filter(conversation__participants=user)
