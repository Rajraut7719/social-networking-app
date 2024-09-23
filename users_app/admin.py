from django.contrib import admin
from users_app.models import User,BlockedUser,FriendRequest,UserActivity
# Register your models here.
admin.site.register(User)
admin.site.register(FriendRequest)
admin.site.register(BlockedUser)
admin.site.register(UserActivity)