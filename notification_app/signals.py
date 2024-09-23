from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save

from users_app.models import FriendRequest
from apis.friend_request.friend_request_api import get_user_by_id
from notification_app.models import Notification

@receiver(post_save, sender=FriendRequest)
def send_friend_request(sender, instance, created, **kwargs):
    """
    Triggered when a new FriendRequest is created to send or update a notification.
    """
    try:
        if created:
            data = {
                'notification_type': 'friend_request_sent',
                'to_user': get_user_by_id(instance.receiver.user_id),
                'from_user': get_user_by_id(instance.sender.user_id),
            }

        # Check if the notification already exists
        notification = Notification.objects.filter(
        notification_type=data['notification_type'],
        to_user=data['to_user'],
        from_user=data['from_user']).first()

        if notification:
            # Update existing notification timestamp
            notification.created_at = timezone.now()
            notification.save()
        else:
           # Creates a new notification if it's not a self-like.
            if instance.receiver.user_id != instance.sender.user_id:
                # Create new notification
                Notification.objects.create(**data)
    except Exception:
        pass
