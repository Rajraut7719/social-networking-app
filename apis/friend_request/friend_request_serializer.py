from rest_framework import serializers
from users_app.models import FriendRequest,User,UserActivity



class PendingUserSerializer(serializers.ModelSerializer):
    """
    This serializer for pending friend request.
    """
    class Meta:
        model = User
        fields = ['user_id', 'username']

class UserActivitySerializer(serializers.ModelSerializer):
    """
    This serializer for User activity log.
    """
    class Meta:
        model = UserActivity
        fields = ['user', 'activity_type', 'timestamp', 'details']