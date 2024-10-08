from rest_framework.generics import GenericAPIView
from rest_framework import status

from post_app.models import PostFiles

from apis.post_app.post_app_serializer import PostFilesSerializer

from utils.success_error_messages.post_app_messages import PostMessages
from utils.api_constants import *
from utils.constant import *
from utils.utility_functions import custom_response, custom_pagination


class AddPostMediaAPI(GenericAPIView):
    """
    This API is for adding new media
    """

    model = PostFiles
    serializer_class = PostFilesSerializer

    def post(self, request):
        """
        API for add feed media.

        URL : POST api/content/post/add-media/

        Request :
        {
            "media_url": FieldField, **required
            "media_type": CharField **required
        }
        Sample Request :
        {
            "media_url": FieldField, **required
            "media_type": CharField **required
        }

        Sample Response :
        {
            "status_code": 200,
            "error": false,
            "data": {
                "media_url": "https://socialnetworkbackend.s3.ap-south-1.amazonaws.com/flowers_yellow_blossom_windy_nature_434.mp4",
                "media_type": "video",
                "media_thumbnail_url": null,
                "post_file_id": [
                    8
                ],
                "created_at": "2024-10-08T13:48:20.601603Z"
            },
            "message": ""
        }
        """
        data = request.data
        response_data = {}
        post_file_uuid = []

        if not data:
            return custom_response(
                status.HTTP_400_BAD_REQUEST, message=PostMessages.ERROR_MEDIA_REQUIRED
            )

        if not request.FILES.getlist(MEDIA_URL):
            return custom_response(
                status.HTTP_400_BAD_REQUEST, message=PostMessages.ERROR_MEDIA_REQUIRED
            )

        post_file_serializer = self.serializer_class(data=data)
        if post_file_serializer.is_valid(raise_exception=True):
            post_file_serializer.save()
            post_file_uuid.append(post_file_serializer.data[POST_FILE_ID])

        response_data = post_file_serializer.data
        response_data[POST_FILE_ID] = post_file_uuid
        return custom_response(status.HTTP_200_OK, response_data, error=False)
