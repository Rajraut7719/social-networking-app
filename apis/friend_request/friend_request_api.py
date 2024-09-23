from django.db import transaction
from django.conf import settings
from django.core.cache import cache
from django.db.models import OuterRef, Subquery
from rest_framework.generics import GenericAPIView
from rest_framework import status

from users_app.models import User,BlockedUser,FriendRequest,UserActivity
from utils.utility_functions import custom_response,custom_pagination
from apis.user_authentication.user_authentication_serializer import GetUsersSerializer
from apis.friend_request.friend_request_serializer import PendingUserSerializer,UserActivitySerializer


def get_user_by_id(user_id):
    try:
        return User.objects.get(user_id=user_id)
    except Exception:
        return None


class FriendRequestAPI(GenericAPIView):
    """
    API for managing friend requests:
    1. Send a friend request
    2. Accept a friend request
    3. Reject a friend request

    Request Format:
    POST http://127.0.0.1:8000/api/friend-requests/
    
    Body:
        {
            "action": "send" | "accept" | "reject",
            "receiver_id": <user_id>
        }

    Responses:
        {
            "status_code": <code>,
            "error": <boolean>,
            "data": {},
            "message": "<response_message>"
        }
    """
    def post(self,request):
        """
        URL POST :- http://127.0.0.1:8000/api/friend-requests/
        Body:
        {
            "action":"send",
            "receiver_id":1
        }

        Response:
        {
            "status_code": 200,
            "error": true,
            "data": {},
            "message": "Friend request sent."
        }
        * Note *
            Authentication token is not required.
    
        """
        action = request.data.get('action')
        receiver_id = request.data.get('receiver_id')
        data = request.data

        if 'receiver_id' not  in data:
            return  custom_response(status.HTTP_400_BAD_REQUEST,error=False,message='Receiver user id required.')
        

        if action not in ['send','accept','reject']:
            return  custom_response(status.HTTP_400_BAD_REQUEST,error=False,message='Please pass valid parameter.')
        
        try:
            receiver = User.objects.get(user_id=receiver_id)
        except Exception:
            return custom_response(status.HTTP_400_BAD_REQUEST,error=True,message='The user you are trying to block does not exist.')
        
        # Check if the user is blocked
        if BlockedUser.objects.filter(blocked_by=request.user,blocked_user=receiver).exists():
            return custom_response(status.HTTP_400_BAD_REQUEST,error=False,message='User has already blocked.')
        
        # Perform the requested action
        if action =='send':
            return self.send_request(request.user,receiver)
        
        elif action =='accept':
            return self.accept_request(request.user,receiver)
        
        elif action =='reject':
            return self.reject_request(request.user,receiver)
    
    def send_request(self,sender,receiver):
        """Send a friend request from sender to receiver."""
        if not FriendRequest.can_send_request(sender, receiver):
            return custom_response(status.HTTP_429_TOO_MANY_REQUESTS,error=False,message='You cannot send a request now. Try later.')
        
         # Check if already sent or received a request
        if FriendRequest.objects.filter(sender=sender, receiver=receiver, status='pending').exists():
            return custom_response(status.HTTP_400_BAD_REQUEST,error=False,message='Friend request already sent.')
        
        # Create friend request
        with transaction.atomic():
            FriendRequest.objects.create(sender=sender, receiver=receiver)
        
        return custom_response(status.HTTP_200_OK,error=True,message='Friend request sent.')
    
    def reject_request(self,sender,receiver):
        """Reject a pending friend request."""
        friend_request = FriendRequest.objects.filter(sender=receiver,receiver=sender).first()
        if not friend_request:
            return custom_response(status.HTTP_404_NOT_FOUND,error=True,message='No pending request found.')
        with transaction.atomic():
            friend_request.status = 'rejected'
            friend_request.save()
        
        return custom_response(status.HTTP_200_OK,error=True,message='Friend request rejected.')
    
    def accept_request(self,sender,receiver):
        """Accept a pending friend request."""
        friend_request  = FriendRequest.objects.filter(sender=receiver,receiver=sender,status='pending').first()
        if not friend_request:
            return custom_response(status.HTTP_404_NOT_FOUND,error=True,message='No pending request found.')
        with transaction.atomic():
            friend_request.status = 'accepted'
            friend_request.save()
        
        return custom_response(status.HTTP_200_OK,error=True,message='Friend request accepted.')
    


class FriendsListAPI(GenericAPIView):
    """
    API to retrieve the list of accepted friends for a user.
    Uses caching to improve performance for frequent queries.
    Allows cache refresh via query parameter.
    """

    friend_request_model = FriendRequest
    user_model = User
    serializer_class = GetUsersSerializer


    def get(self,request):
        """
        Handles GET requests to retrieve the user's accepted friends list.
        If the 'is_refresh' parameter is set to 'true', the cache is cleared and refreshed.
        Otherwise, the cached data is returned to optimize performance.

        URL POST :- http://127.0.0.1:8000/api/friend-requests/
    
        URL POST :- http://127.0.0.1:8000/api/friend-requests/?is_refresh=true
    
        Response:
        {
            "status_code": 200,
            "error": true,
            "links": {
                "next": null,
                "previous": null
            },
            "count": 3,
            "data": [
                {
                    "user_id": 12,
                    "username": "python",
                    "email": "python@gmail.com"
                },
                {
                    "user_id": 3,
                    "username": "raj",
                    "email": "raj@gmail.com"
                },
                {
                    "user_id": 6,
                    "username": "radha",
                    "email": "radha@gmail.com"
                }
            ],
            "message": ""
        }
        * Note *
            Authentication token is not required.
    
        """

        # Cache key based on the user's ID
        cache_key = f"friends_list_{request.user.user_id}"
        # Check if cache needs refreshing
        is_refresh = request.GET.get('is_refresh', None)

        get_page_size = 50
        user = request.user

        # Delete cache if refresh is requested
        if is_refresh == 'true':
            cache.delete(cache_key)
        
        # Try to retrieve cached data
        response = cache.get(cache_key)

        if response is None:

            # Get IDs of users who have accepted the friend request from the current user
            user_id = self.friend_request_model.objects.filter(receiver=user,status='accepted').values_list('sender__user_id',flat=True)
            # Fetch user data for the accepted friends
            user_queryset = self.user_model.objects.filter(user_id__in=[user_id])
        
            #return data in pagination
            response = custom_pagination(
                get_page_size=get_page_size,
                request=request,
                serializer_class=self.serializer_class,
                queryset=user_queryset,
            )

            # Cache the response for 30 minutes
            cache.set(cache_key, response, timeout=settings.CACHE_TIMEOUT)
            
        return custom_response(status.HTTP_200_OK,response,error=True,is_pagination=True)

class PendingRequest(GenericAPIView):
    """
    API view to retrieve a list of pending friend requests received by the user.

    This API returns users who have sent friend requests to the current user,
    ordered by the time the requests were created (most recent first).
    
    """
    user_model = User
    friend_request_model = FriendRequest
    serializer_class = PendingUserSerializer
    def get(self,request):
        """
        Handle GET requests to retrieve pending friend requests.

        Query Parameters:
        - page_size: Optional. Number of results per page for pagination.

        Response:
        {
            "status_code": 200,
            "error": true,
            "links": {
                "next": null,
                "previous": null
            },
            "count": 5,
            "data": [
                {
                "user_id": 1,
                "username": "nilesh"
                },
                {
                "user_id": 9,
                "username": "rakesh"
                },
            ],
            "message": ""
            }
            * Note *
            Authentication token is not required.
        """
        get_page_size = request.GET.get('page_size', None)
        user = request.user
        
        # Retrieve all pending friend requests for the current user,
        # sorted by the creation time in descending order (most recent first)
        pending_requests = self.friend_request_model.objects.filter(receiver=user, status='pending').order_by('-created_at')
        user_ids = pending_requests.values_list('sender__user_id', flat=True)

        # Get the user queryset based on the sender IDs,
        # ordered by the creation time of their friend requests in descending order
        user_queryset = self.user_model.objects.filter(user_id__in=user_ids).annotate(
            request_created_at=Subquery(
                pending_requests.filter(sender__user_id=OuterRef('user_id')).values('created_at')[:1]
            )
        ).order_by('-request_created_at')

        # return data in pagination
        response = custom_pagination(
            get_page_size=get_page_size,
            request=request,
            serializer_class=self.serializer_class,
            queryset=user_queryset,
        )    
        return custom_response(status.HTTP_200_OK,response,error=True,is_pagination=True)


class UserActivityLogAPI(GenericAPIView):
    """
    API for log and retrieve user activities.
    """
    model = UserActivity
    serializer_class = UserActivitySerializer

    def post(self,request):
        """
        Log a new user activity.

        Request Body:
        - activity_type: Type of activity (e.g., 'friend_request_sent', 'friend_request_accepted')
        - details: Optional additional details about the activity

        URL :POST : http://127.0.0.1:8000/api/user-activities/

        Body:
        {
            "activity_type": "friend_request_sent",
            "details": "Sent a friend request"
        }

        Response:
        {
            "status_code": 201,
            "error": true,
            "data": {
                "user": 2,
                "activity_type": "friend_request_sent",
                "timestamp": "2024-09-23T09:51:15.007572Z",
                "details": "Sent a friend request"
            },
            "message": ""
        }
        * Note *
            Authentication token is not required.
        """
        activity_type = request.data.get('activity_type')
        details = request.data.get('details', '')

        if not activity_type:
            return custom_response(status.HTTP_400_BAD_REQUEST,error=False,message='Activity type is required.')
        
        # Create and save the activity log
        activity = UserActivity.objects.create(user=request.user, activity_type=activity_type, details=details)
        response = self.serializer_class(activity).data

        return custom_response(status.HTTP_201_CREATED,response,error=True)
    
    def get(self,request):
        """
        Retrieve all activities for the authenticated user.

        URL GET: http://127.0.0.1:8000/api/user-activities/

        Response:
        {
            "status_code": 201,
            "error": true,
            "data": [
                {
                "user": 2,
                "activity_type": "friend_request_sent",
                "timestamp": "2024-09-23T09:57:58.878681Z",
                "details": "Sent a friend request"
                },
                {
                "user": 2,
                "activity_type": "friend_request_sent",
                "timestamp": "2024-09-23T09:57:57.652482Z",
                "details": "Sent a friend request"
                },
            ],
            "message": ""
        }

        """
        activities = self.model.objects.filter(user=request.user).order_by('-timestamp')
        serializer = self.serializer_class(activities, many=True)
        response = serializer.data
        return custom_response(status.HTTP_201_CREATED,response,error=True)



    


        










        



            




        

        
    
