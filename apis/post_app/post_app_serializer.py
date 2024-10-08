from rest_framework import serializers
from post_app.models import PostFiles
from utils.constants.model_constants.post_app_constants import *


class PostFilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostFiles
        fields = (
            POST_FILES_FIELD_MEDIA_URL,
            POST_FILES_FIELD_MEDIA_TYPE,
            POST_FILES_FIELD_MEDIA_THUMBNAIL_URL,
            POST_FILES_FIELD_ID,
            POST_FILES_FIELD_CREATED_DATE,
        )
