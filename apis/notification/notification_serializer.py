from rest_framework import serializers
from apis.user_authentication.user_authentication_api import GetUsersSerializer
from notification_app.models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    """
    Serializer for notification
    """
    from_user_data = GetUsersSerializer(source='from_user')
    to_user_data = GetUsersSerializer(source='to_user')

    class Meta:
        model = Notification
        exclude = ('notification_id','from_user','to_user')


