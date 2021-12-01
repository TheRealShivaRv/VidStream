from django.contrib import admin
from accounts.models import EmailVerification
class EmailVerificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'requestid', 'purpose')    
admin.site.register(EmailVerification,EmailVerificationAdmin)
