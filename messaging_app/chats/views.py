from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

class ConversationViewSet(viewsets.ModelViewSet):
    """ViewSet for listing and creating conversations."""
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """Save the conversation and set participants."""
        conversation = serializer.save()
        # Add the requesting user as a participant (optional, depending on requirements)
        conversation.participants.add(self.request.user)

    def get_queryset(self):
        """Return conversations where the user is a participant."""
        return Conversation.objects.filter(participants=self.request.user)

class MessageViewSet(viewsets.ModelViewSet):
    """ViewSet for listing and sending messages."""
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """Save the message with the requesting user as sender."""
        serializer.save(sender=self.request.user)

    def get_queryset(self):
        """Optionally filter messages by conversation_id from query params."""
        queryset = Message.objects.filter(conversation__participants=self.request.user)
        conversation_id = self.request.query_params.get('conversation_id')
        if conversation_id:
            queryset = queryset.filter(conversation__conversation_id=conversation_id)
        return queryset