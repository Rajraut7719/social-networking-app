from django.db import models
from users_app.mixin import BaseModleMixin
from utils.constant import *
from utils.utility_functions import path_and_rename
from users_app.models import User


# Create your models here.
class PostType(BaseModleMixin):
    POST_TYPE_CHOICES = (
        (MEDIA_TYPE_IMAGE, MEDIA_TYPE_IMAGE),
        (MEDIA_TYPE_VIDEO, MEDIA_TYPE_VIDEO),
        (MEDIA_TYPE_CAROUSEL, MEDIA_TYPE_CAROUSEL),
        (MEDIA_TYPE_REELS, MEDIA_TYPE_REELS),
    )

    post_type_id = models.AutoField(primary_key=True, null=False)
    post_type = models.CharField(max_length=30, choices=POST_TYPE_CHOICES)

    def __str__(self):
        return f"Post Type ID : {self.post_type_id} -> Post Type: {self.post_type}"


class Post(BaseModleMixin):
    post_id = models.AutoField(primary_key=True, null=False, blank=False)
    post_caption = models.TextField(max_length=1600, null=True, blank=True)
    post_type = models.ForeignKey(PostType, on_delete=models.CASCADE)
    posted_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name=POST_POSTED_BY_MODEL_MANAGER
    )
    is_comment_allowed = models.BooleanField(default=True)
    is_post_share_as_msg_allowed = models.BooleanField(default=True)
    is_liked_allowed = models.BooleanField(default=True)
    is_saved_allowed = models.BooleanField(default=True)
    is_post_share_on_other_platform_allowed = models.BooleanField(default=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f" Post ID : {self.post_id} -> Posted By : {self.posted_by.username} -> Post Type : {self.post_type}"


class PostFiles(BaseModleMixin):
    post_file_id = models.AutoField(primary_key=True, null=False, blank=False)
    media_url = models.FileField(
        upload_to=path_and_rename, max_length=2000, null=True, blank=True
    )
    media_type = models.CharField(max_length=30, null=False, blank=False)
    media_thumbnail_url = models.URLField(null=True, max_length=500)
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name=POST_FILES_POST_MODEL_MANAGER,
        null=True,
    )

    def __str__(self):
        return f"Post File UUID : {self.post_file_id} -> Post UUID : {self.post} -> Media Type : {self.media_type}"
