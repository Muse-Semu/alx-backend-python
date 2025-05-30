from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    """Custom user model extending AbstractUser with additional fields."""
    bio = models.TextField(max_length=500, blank=True, null=True, help_text="Short user biography")
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True, help_text="User profile picture")
    
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.username

class Conversation(models.Model):
    """Model to represent a conversation between multiple users."""
    participants = models.ManyToManyField(
        User,
        related_name='conversations',
        help_text="Users participating in this conversation"
    )
    created_at = models.DateTimeField(default=timezone.now, help_text="When the conversation was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the conversation was last updated")

    class Meta:
        verbose_name = "Conversation"
        verbose_name_plural = "Conversations"
        ordering = ['-updated_at']

    def __str__(self):
        return f"Conversation {self.id} with {', '.join(participant.username for participant in self.participants.all())}"

class Message(models.Model):
    """Model to represent a message in a conversation."""
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages',
        help_text="The conversation this message belongs to"
    )
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_messages',
        help_text="The user who sent this message"
    )
    content = models.TextField(max_length=2000, help_text="Message content")
    created_at = models.DateTimeField(default=timezone.now, help_text="When the message was sent")
    is_read = models.BooleanField(default=False, help_text="Whether the message has been read")

    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"
        ordering = ['created_at']

    def __str__(self):
        return f"Message from {self.sender.username} in Conversation {self.conversation.id}"