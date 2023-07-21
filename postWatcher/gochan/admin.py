from django.contrib import admin
from .models import Post


# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = (
        'id','keyword', 'alreadyRead', 'title', 'userId', 'postDate', 'searchPlace', 'postBody', 'userUrl', 'postUrl', 'otherUrl',
        'wordNotification', 'created_at', 'updated_at')


admin.site.register(Post, PostAdmin)
