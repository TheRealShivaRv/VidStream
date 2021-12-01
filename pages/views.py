from django.shortcuts import render
from videos.models import Video, Like
from django.contrib.auth.models import User
def index(request):
    if request.user.is_authenticated:
        videos = Video.objects.all()
        likes = Like.objects.all()
        videotitles = []
        for like in likes:
            if like.username == request.user.username:
                title = str(like.videotitle)
                videotitles.append(title)
        context = {
            'videos': videos,
            'likes': likes,
            'videotitles': videotitles
        }
        return render(request, 'pages/index.html', context)
    else:
        videos = Video.objects.all()
        context = {
            'videos': videos
        }
        return render(request, 'pages/index.html', context)
