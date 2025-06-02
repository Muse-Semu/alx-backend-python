from rest_framework import permissions
from .models import Conversation, Message

class IsOwnerOrParticipant(permissions.BasePermission):
    """Custom permission to ensure users access only their own conversations and messages."""
    
    def has_permission(self, request, view):
        """Check if the user is authenticated."""
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """Check if the user is a participant in the conversation or the message sender."""
        if isinstance(obj, Conversation):
            return obj.participants.filter(user_id=request.user.user_id).exists()
        elif isinstance(obj, Message):
            # Allow access if the user is the sender or a participant in the conversation
            return obj.sender == request.user or obj.conversation.participants.filter(user_id=request.user.user_id).exists()
        return False