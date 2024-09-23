from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from users_app.custome_throttle import LoginThrottle
from users_app.models import User

from django.contrib.auth import authenticate
from django.db.models import Q
from utils.utility_functions import custom_response,custom_pagination
from users_app.custom_permission import RoleBasedPermission
from apis.user_authentication.user_authentication_serializer import SignUpSerializer,GetUsersSerializer


class SignUpAPI(GenericAPIView):
    """
    User can sign up using this api.
    """

    authentication_classes = ()
    permission_classes = ()
    serializer_class = SignUpSerializer

    def post(self, request):
        """
        URL : http://127.0.0.1:8000/api/sign-up/

        parameters:
        {
            "email": "EmailField" **Required
            "password": "CharField" **Required
        }

        Sample parameters:
        {
            "email": "rajraut@gmail.com",
            "password":"Qwerty@123"
        }

        Response:
        {
            "status_code": 201,
            "error": false,
            "data": {
                "user_id": 1,
                "email": "rajraut@gmail.com"
            },
            "message": "User created successfully."
        }
        * Note *
            Authentication token is not required.

        """
        response_data = {}
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()

        get_user = User.objects.filter(email__iexact=user.email).first()

        response_data["user_id"] = get_user.user_id
        response_data["email"] = get_user.email
        return custom_response(
            status.HTTP_201_CREATED,
            response_data,
            error=False,
            message="User created successfully.",
        )


class UserLoginAPI(GenericAPIView):
    """
    User can login using this api.
    """
    authentication_classes = ()
    permission_classes = ()
    throttle_classes = [LoginThrottle]

    def post(self, request):
        """
        URL : http://127.0.0.1:8000/api/login/

        parameters:
        {
            "email": "EmailField" **Required
            "password": "CharField" **Required
        }

        Sample parameters:
        {
            "email": "rajraut@gmail.com",
            "password":"Qwerty@123"
        }

        Response:
        {
            "status_code": 200,
            "error": false,
            "data": {
                "user_id": 14,
                "email": "babu@gmail.com",
                "refresh": [
                    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcyNjkxNTA1NiwiaWF0IjoxNzI2ODI4NjU2LCJqdGkiOiJkM2Q4ZDYzODk3MTU0ZWJmYjI1MjdjNzhmYjJjNGEzOSIsInVzZXJfaWQiOjE0fQ.Jr4NqcNqRWn0_InoRgydNuYQgEN0rEHH9xUjteFiGYM"
                ],
                "access": [
                    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzI2ODM1ODU2LCJpYXQiOjE3MjY4Mjg2NTYsImp0aSI6IjBlMThhZWYwOWExODRiMDA4MzRiYWUyM2JhYThiY2FiIiwidXNlcl9pZCI6MTR9.WBQsEayihVxNFGrQqjCpMNaspiAp9oythEWJ4O9btTA"
                ]
            },
            "message": "You successfully logged in"
        }
        * Note *
            Authentication token is required.

        
        Users can attempt to log in up to five times per hour. If more than five attempts are made,
        the following message will be displayed:
        {
            "detail": "Too many login attempts. Please try again 59 minutes, and 48 seconds."
        }


        """
        response_data = {}
        request_data = request.data

        email = request_data.get("email")
        password = request_data.get("password")

        user = authenticate(request, username=email, password=password)

        if not user or (not user.is_active):
            return custom_response(
                status.HTTP_401_UNAUTHORIZED,
                message="Please check email and password",
            )
        
        # create token for user
        refresh = RefreshToken.for_user(user)

        response_data["user_id"] = user.user_id
        response_data["email"] = user.email
        response_data["refresh"] = str(refresh),
        response_data["access"] = str(refresh.access_token),

        return custom_response(
            status.HTTP_200_OK,
            response_data,
            error=False,
            message="You successfully logged in",
        )


class GetUsers(GenericAPIView):
    """
    Api for get user data
    """
    model = User
    serializer_class = GetUsersSerializer
    permission_classes = [RoleBasedPermission,]
    def get(self,request):
        """
        URL : http://127.0.0.1:8000/api/get_user/

        ## it  return 10 records bydefault

        ## if I pass page_size in PARM, 
        URL : http://127.0.0.1:8000/api/get_user/?page_size=2

        Response:
        {
            "status_code": 200,
            "error": false,
            "links": {
                "next": "http://127.0.0.1:8000/api/get_user/?page=2&page_size=2",
                "previous": null
            },
            "count": 12,
            "data": [
                {
                    "username": "admin",
                    "email": "admin@gmail.com"
                },
                {
                    "username": null,
                    "email": "babu@gmail.com"
                }
            ],
            "message": ""
        }

        ## when I will pass search parameter in PARAM.

        URL : http://127.0.0.1:8000/api/get_user/?search=raj@gmail.com

        Response:
        {
            "status_code": 200,
            "error": false,
            "links": {
                "next": null,
                "previous": null
            },
            "count": 1,
            "data": [
                {
                    "username": rajraut,
                    "email": "raj@gmail.com"
                }
            ],
            "message": ""
        }

        ## when I will pass seach parameter contains in PARAM.

        URL : http://127.0.0.1:8000/api/get_user/?search=ra

        Response:
        {
            "status_code": 200,
            "error": false,
            "links": {
                "next": null,
                "previous": null
            },
            "count": 3,
            "data": [
                {
                    "username": rajraut,
                    "email": "raj@gmail.com"
                },
                {
                    "username": rajesh,
                    "email": "rajesh@gmail.com"
                },
                {
                    "username": radha,
                    "email": "radha@gmail.com"
                },
            ],
            "message": ""
        }
        * Note *
            Authentication token is not required.
    
        """

        get_page_size = request.GET.get('page_size', None)
        search = request.GET.get('search',None)
        
        # retrive those records is_active = True
        queryset = self.model.objects.filter(is_active=True)

        # filter records based on email or username
        if search:
            queryset = queryset.filter(Q(email__icontains=search) |Q(username__icontains=search))

        #return data in pagination
        response = custom_pagination(
            get_page_size=get_page_size,
            request=request,
            serializer_class=self.serializer_class,
            queryset=queryset,
        )
        return custom_response(
            status.HTTP_200_OK, response, error=False,is_pagination=True
        )

