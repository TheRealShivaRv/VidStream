from django.db import models

class EmailVerification(models.Model):
    username = models.CharField(max_length=256, unique=True)
    email = models.CharField(max_length=256)
    requestid = models.CharField(max_length=256)
    purpose = models.CharField(max_length=256)
    def __str__(self):
        return self.requestid
