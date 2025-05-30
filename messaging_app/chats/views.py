from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer

class ConversationViewSet(viewsets.ModelViewSet):
    """ViewSet for listing and creating conversations with filtering."""
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['participants']  # Allow filtering by participant user_id

    def perform_create(self, serializer):
        """Save the conversation and set participants."""
        conversation = serializer.save()
        conversation.participants.add(self.request.user)

    def get_queryset(self):
        """Return conversations where the user is a participant."""
        return Conversation.objects.filter(participants=self.request.user)

class MessageViewSet(viewsets.ModelViewSet):
    """ViewSet for listing and sending messages with filtering."""
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['conversation']  # Allow filtering by conversation_id

    def perform_create(self, serializer):
        """Save the message with the requesting user as sender."""
        serializer.save(sender=self.request.user)

    def get_queryset(self):
        """Return messages from conversations the user is part of."""
        return Message.objects.filter(conversation__participants=self.request.user)