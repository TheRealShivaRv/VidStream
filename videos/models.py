from django.db import models
from django.contrib.auth.models import User
class Video(models.Model):
    title = models.CharField(max_length=256)
    description = models.TextField(null=True)
    video = models.FileField(upload_to='uploads/videos/')
    thumbnail = models.ImageField(upload_to='uploads/thumbnails/')
    uploader = models.CharField(max_length=256)
    def __str__(self):
        return self.title
class Like(models.Model):
    username = models.CharField(max_length=256, blank=False)
    videotitle = models.CharField(max_length=256, blank=False)
    is_liked = models.BooleanField(default=False)
    def __str__(self):
        return self.videotitle
