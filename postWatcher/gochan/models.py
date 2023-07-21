from django.db import models


# Create your models here.
class Post(models.Model):
    keyword = models.CharField(max_length=255)
    userId = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    postDate = models.DateTimeField()
    postBody = models.CharField(max_length=255)
    alreadyRead = models.CharField(max_length=255, default='FALSE')
    wordNotification = models.CharField(max_length=255, default='FALSE')
    postUrl = models.URLField(null=True)
    userUrl = models.URLField(null=True)
    otherUrl = models.URLField(null=True)
    searchPlace = models.CharField(max_length=255, default='5ch(2ch)')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.title
