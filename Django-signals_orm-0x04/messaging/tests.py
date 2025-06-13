from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification
from django.utils import timezone

class MessagingTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='pass123')
        self.user2 = User.objects.create_user(username='user2', password='pass123')
        
    def test_message_creation(self):
        message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content="Hello, this is a test message!"
        )
        self.assertEqual(message.sender, self.user1)
        self.assertEqual(message.receiver, self.user2)
        self.assertEqual(message.content, "Hello, this is a test message!")
        self.assertTrue(abs(message.timestamp - timezone.now()).total_seconds() < 1)
        
    def test_notification_creation_on_message(self):
        message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content="Test notification message"
        )
        notification = Notification.objects.get(user=self.user2, message=message)
        self.assertEqual(notification.user, self.user2)
        self.assertEqual(notification.message, message)
        self.assertFalse(notification.is_read)
        self.assertTrue(abs(notification.created_at - timezone.now()).total_seconds() < 1)
        
    def test_no_notification_for_sender(self):
        Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content="No notification for sender"
        )
        self.assertFalse(Notification.objects.filter(user=self.user1).exists())