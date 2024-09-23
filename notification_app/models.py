from django.db import models
from users_app.models import BaseModleMixin,User
# Create your models here.
class Notification(BaseModleMixin):
    
    NOTIFICATION_TYPES = [
        ('friend_request_sent', 'friend_request_sent'),
        ('friend_request_accepted', 'friend_request_accepted'),
        
    ]

    notification_id = models.AutoField(primary_key=True,null=False,blank=False)
    notification_type = models.CharField(max_length=100,choices=NOTIFICATION_TYPES,blank=False, null=False)
    from_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notification_from_user_model_manager',
        blank=False,
        null=False,
    )
    to_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notification_to_user_model_manager',
        blank=False,
        null=False,
    )
    read_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Notification ID : {self.notification_id} -> Notification Type : {self.notification_type} -> To User ID : {self.to_user.user_id} -> From User ID : {self.from_user.user_id}"

