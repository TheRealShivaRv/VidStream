from django.contrib import admin
from .models import Video, Like
class VideoAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'uploader', 'thumbnail', 'video', 'description')
    list_display_links = ('id', 'title','uploader', 'video', 'thumbnail')
    list_display = ('id', 'title', 'uploader', 'description', 'thumbnail', 'video')
    list_display_links = ('id', 'title')
    list_filter = ('uploader',)
    search_fields = ('title', 'uploader')
    list_per_page = 25
admin.site.register(Video, VideoAdmin)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'videotitle', 'is_liked')
    list_display_links = ('username', 'videotitle')

admin.site.register(Like, LikeAdmin)
