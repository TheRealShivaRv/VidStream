from django import forms
from django.contrib.auth.models import User
class UploadFileForm(forms.Form):
    title = forms.CharField()
    description = forms.CharField()
    video = forms.FileField()
    thumbnail = forms.ImageField()
    uploader = forms.CharField()
    def __str__(self):
        self.title
class LikeForm(forms.Form):
    username = forms.CharField(max_length=256)
    videotitle = forms.CharField(max_length=256)
    is_liked = forms.BooleanField()
    def __str__(self):
        self.is_liked
