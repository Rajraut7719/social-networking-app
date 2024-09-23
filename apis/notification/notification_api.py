from rest_framework.generics import GenericAPIView
from rest_framework import status
from django.utils import timezone
from utils.utility_functions import custom_response,custom_pagination
from notification_app.models import Notification
from apis.notification.notification_serializer import NotificationSerializer

class NotificationListAPI(GenericAPIView):
    """
    API to list notifications for the logged-in user, grouped by today, yesterday, and last 7 days.
    """
    model = Notification
    serializer_class = NotificationSerializer

    def get(self,request):
        """
        GET endpoint to retrieve user notifications.
        Groups notifications into today, yesterday, and last 7 days.

        URL: http://127.0.0.1:8000/api/notifications-list/

        Response:
        {
            "status_code": 200,
            "error": false,
            "today": [
                {
                "from_user_data": {
                    "user_id": 7,
                    "username": "dinesh",
                    "email": "dinesh@gmail.com"
                },
                "to_user_data": {
                    "user_id": 2,
                    "username": "babu",
                    "email": "babu@gmail.com"
                },
                "created_at": "2024-09-23T11:24:49.133473Z",
                "updated_at": "2024-09-23T11:24:49.133473Z",
                "notification_type": "friend_request_sent",
                "read_at": null
                }
            ],
            "yesterday": [],
            "last_7_days": [],
            "message": ""
        }
        
        """
        user = request.user
        today = timezone.now().date()
        yesterday = timezone.now().date() - timezone.timedelta(days=1)
        last_7_days = timezone.now().date() - timezone.timedelta(days=7)
        context = {'user': user}

        # Start with notifications for the user, excluding self-notifications
        users_notification = self.model.objects.filter(to_user=user).exclude(
            from_user=user
        )

        # Prepare data grouped by time 
        data = {
            'today':self.get_notifications_for_day(
                users_notification, today, context
            ),
            'yesterday':self.get_notifications_for_day(
                users_notification, yesterday, context
            ),
            'last_7_days':self.get_notifications_for_last_week(
                users_notification, last_7_days, context
            ),
        }
        return custom_response(
            status.HTTP_200_OK, data, error=False, is_pagination=True
        )
    
    def get_notifications_for_day(self, users_notification, day, context):
        # Filter and order notifications by the specified day
        notifications = users_notification.filter(created_at__date=day).order_by('-created_at')
        return self.serializer_class(notifications, context=context, many=True).data
    
    def get_notifications_for_last_week(self, users_notification, last_7_days, context):
        """
        Get notifications from the last 7 days.
        
        Args:
            users_notification (QuerySet): Filtered notifications.
            last_7_days (datetime.date): Date for one week ago.
            context (dict): Context for the serializer.
        """
        # Filter and order notifications for the last 7 days, limit to 50 results
        notifications = users_notification.filter(
            created_at__date=last_7_days
        ).order_by('-created_at')[:50]

        # Serialize the notifications data
        return self.serializer_class(notifications, context=context, many=True).data


class NotificationReadAPI(GenericAPIView):
    """
    API for notification read.

    URL GET : api/notifications-read/
    {
        "status_code": 200,
        "error": false,
        "data": {},
        "message": ""
    }
    """
    model = Notification

    def get(self,request):
        self.model.objects.filter(to_user=request.user,read_at__isnull=True).update(read_at=timezone.now())
        return custom_response(status.HTTP_200_OK, error=False)


