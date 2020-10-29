from django import forms
from django.contrib.auth.models import User

class UserUpdateForm(forms.Form):
    id = forms.IntegerField()
    username = forms.CharField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.CharField()
    password = forms.CharField(max_length=32, widget=forms.PasswordInput)
    def __str__(self):
        self.username
