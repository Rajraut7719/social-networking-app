from django.urls import path
from apis.user_authentication.user_authentication_api import SignUpAPI, UserLoginAPI,GetUsers
from apis.friend_request.friend_request_api import FriendRequestAPI,FriendsListAPI,PendingRequest,UserActivityLogAPI
from apis.notification.notification_api import NotificationListAPI,NotificationReadAPI
urlpatterns = [
    path("sign-up/", SignUpAPI.as_view()),
    path("login/", UserLoginAPI.as_view()),
    path('get_user/',GetUsers.as_view()),
    path('friend-requests/',FriendRequestAPI.as_view()),
    path('friends_list/', FriendsListAPI.as_view()),
    path('pending-requests/',PendingRequest.as_view()),
    path('user-activities/',UserActivityLogAPI.as_view()),
    # Notification
    path('notifications-list/',NotificationListAPI.as_view()),
    path('notifications-read/',NotificationReadAPI.as_view())
]
