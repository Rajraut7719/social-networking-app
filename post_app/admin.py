from django.contrib import admin
from .models import Post, PostType, PostFiles

# Register your models here.
admin.site.register(Post)
admin.site.register(PostFiles)
admin.site.register(PostType)
