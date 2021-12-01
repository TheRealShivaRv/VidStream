from django.urls import path
from . import views
urlpatterns = [
    path('video/<str:videotitle>', views.video, name='video'),
    path('upload', views.upload, name='upload'),
    path('search', views.search, name='search'),
    path('videolike', views.videolike, name='videolike'),
    path('videosettings/<str:videotitle>', views.videosettings, name='videosettings'),
    path('videoupdate', views.videoupdate, name='videoupdate'),
    path('videodelete/<str:videotitle>',views.videodelete, name='videodelete')
]
