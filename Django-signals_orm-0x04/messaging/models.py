from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

User = get_user_model()

class MessageHistory(models.Model):
    """Stores historical versions of edited messages"""
    original_message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        related_name='edits'
    )
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)
    edited_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='message_edits'
    )

    class Meta:
        ordering = ['-edited_at']
        verbose_name_plural = "Message History"

    def __str__(self):
        return f"Edit of {self.original_message} at {self.edited_at}"


    
class Message(models.Model):
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messaging_sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messaging_received_messages')
    
    content = models.TextField(max_length=2000)
    timestamp = models.DateTimeField(default=timezone.now)
    read = models.BooleanField(default=False)  # New field
    parent_message = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    edited = models.BooleanField(default=False)
    last_edited = models.DateTimeField(null=True, blank=True)

    # Managers
    objects = models.Manager()  # Default manager
    unread = UnreadMessagesManager()  # Custom manager for unread messages


    def mark_as_read(self):
        """Helper method to mark a message as read"""
        self.read = True
        self.save(update_fields=['read'])


    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['parent_message']),
            models.Index(fields=['sender', 'receiver']),
            models.Index(fields=['read']),  # Index for better performance
            models.Index(fields=['receiver', 'read']),
        ]

    def __str__(self):
        return f"Message from {self.sender.username}"

    def get_thread(self):
        """Returns the root message of the thread"""
        return self.parent_message.get_thread() if self.parent_message else self

    @property
    def is_reply(self):
        return self.parent_message is not None



class MessageQuerySet(models.QuerySet):
    def with_related_data(self):
        """Optimized query with all related data"""
        return self.select_related(
            'sender',
            'receiver',
            'parent_message__sender'
        ).prefetch_related(
            Prefetch('replies', queryset=Message.objects.select_related('sender'))
        )

    def get_conversation_threads(self, user1, user2):
        """Get all message threads between two users"""
        return self.filter(
            models.Q(sender=user1, receiver=user2) |
            models.Q(sender=user2, receiver=user1),
            parent_message__isnull=True  # Only root messages
        ).with_related_data()

    def get_full_thread(self, root_message_id):
        """Get a complete thread with all replies"""
        return self.filter(
            models.Q(message_id=root_message_id) |
            models.Q(parent_message__message_id=root_message_id)
        ).with_related_data().order_by('timestamp')

# Attach the custom queryset to the model
Message.objects = MessageQuerySet.as_manager()

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Notification for {self.user}: {self.message.content[:50]}"

class MessageHistory(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='history')
    old_content = models.TextField()
    edited_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-edited_at']
    
    def __str__(self):
        return f"Edit history for message {self.message.id} at {self.edited_at}"


