from django.db import models
from django.contrib.auth.models import AbstractUser
from users_app.mixin import BaseModleMixin
from users_app.manager import UserManager

from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta


# User model
class User(AbstractUser, BaseModleMixin):
    user_id = models.AutoField(primary_key=True, null=False, blank=False)
    username = models.CharField(max_length=150, null=True, blank=True, unique=True,db_index=True)
    email = models.EmailField(unique=True,db_index=True)

    objects = UserManager()

    # username = None
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", "password"]

    def __str__(self) -> str:
        return f"ID : {self.user_id} -> {self.email}"

class FriendRequest(BaseModleMixin):
    """
    Model for managing friend requests between users.

    Attributes:
        friend_request_id (int): Unique ID for the friend request.
        receiver (ForeignKey): The user who gets the friend request.
        sender (ForeignKey): The user who sends the friend request.
        status (CharField) it has status - pending,accepted,rejected
    """
    FRIEND_REQUEST = [
        ('pending', 'pending'), 
        ('accepted', 'accepted'), 
        ('rejected', 'rejected')
        ]

    friend_request_id = models.AutoField(primary_key=True,null=False,blank=False)
    sender = models.ForeignKey(User,on_delete=models.CASCADE,related_name='firend_request_sender_model_manager')
    receiver = models.ForeignKey(User,on_delete=models.CASCADE,related_name='firend_request_receiver_model_manager')
    status = models.CharField(max_length=10,choices=FRIEND_REQUEST,default='pending')

    @staticmethod
    def can_send_request(sender, receiver, cooldown_hours=24):
        # Check rate limiting (3 requests per minute)
        one_min_ago = timezone.now() - timedelta(minutes=1)
        sent_count = FriendRequest.objects.filter(sender=sender, created_at__gte=one_min_ago).count()
        if sent_count >= 3:
            return False
        
        # Check cooldown after rejection
        rejection_cooldown = timezone.now() - timedelta(hours=cooldown_hours)
        rejected_recently = FriendRequest.objects.filter(sender=sender, receiver=receiver, status='rejected', updated_at__gte=rejection_cooldown).exists()
        return not rejected_recently
    def __str__(self) -> str:
        return f"ID : {self.friend_request_id} -> Sender :- {self.sender.user_id} recipient :- {self.receiver.user_id} -> Status {self.status}"
    
    class Meta:
        unique_together = ("sender","receiver") 


class BlockedUser(BaseModleMixin):
    """
    Represents a block action where one user blocks another.

     Fields:
    - block_user_id: Unique ID for each block record.
    - blocked_by: The user who is blocking someone.
    - blocked_user: The user who is being blocked.
    """
    block_user_id = models.AutoField(primary_key=True, null=False, blank=False)
    blocked_by = models.ForeignKey(User,on_delete=models.CASCADE,related_name='block_user_blocked_by_model_manager')
    blocked_user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='block_user_blocked_user_model_manager')

    def __str__(self):
        return f"ID : {self.block_user_id} -> Blocked By ID : {self.blocked_by.user_id} -> Blocked User ID : {self.blocked_user.user_id}"
    
    class Meta:
        """
        Ensures each user can block another user only once.
        """
        unique_together = ("blocked_by","blocked_user")


class UserActivity(BaseModleMixin):
    """
    Model to log user activities.

    Attributes:
        user (ForeignKey): The user associated with the activity.
        activity_type (CharField): The type of activity (e.g., 'friend_request_sent', 'friend_request_accepted').
        timestamp (DateTimeField): The time when the activity occurred.
        details (TextField): Any additional details about the activity.
    """
    ACTIVITY_TYPES = [
        ('friend_request_sent', 'friend_request_sent'),
        ('friend_request_accepted', 'friend_request_accepted'),
        ('friend_request_rejected', 'friend_request_rejected')
    ]
    user_activity_id = models.AutoField(primary_key=True, null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_activity_user_model_manager')
    activity_type = models.CharField(max_length=50, choices=ACTIVITY_TYPES)
    timestamp = models.DateTimeField(default=timezone.now)
    details = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.activity_type} on {self.timestamp}"


