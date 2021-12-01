from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.db import models
from django.contrib import messages
from django.contrib.auth.models import User
from videos.forms import UploadFileForm, LikeForm
from videos.models import Video, Like

def upload(request):
    if not request.user.is_authenticated:
        messages.error(request, 'You are not logged in')
        return redirect('login')
    else:
        if request.method == 'POST':
            title = request.POST['title']
            video = request.FILES['video']
            description = request.POST['description']
            thumbnail = request.FILES['thumbnail']
            uploader = request.POST['uploader']
            form = UploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                if not Video.objects.all().filter(title=title).exists():
                    file = Video(video=video, title=title, description=description, thumbnail=thumbnail, uploader=uploader)
                    file.save()
                    messages.success(request,'File Uploaded successfully')
                    return redirect('dashboard')
                else:
                    messages.error(request,'File Upload failed')
                    return redirect('upload')
            else:
                messages.error(request,'File Upload failed')
                return redirect('upload')
        else:
            return render(request, 'videos/upload.html')
def videolike(request):
    if request.method == 'POST':
        username = request.POST['username']
        videotitle = request.POST['videotitle']
        sourceurl = request.POST['sourceurl']
        is_liked = request.POST['is_liked']
        if not username:
            return redirect('login')
        else:
            form = LikeForm(request.POST)
            if form.is_valid():
                if not Like.objects.filter(username=username, videotitle=videotitle).exists():
                    videolike = Like(username=username, videotitle=videotitle, is_liked=is_liked)
                    videolike.save()
                    messages.success(request, 'You liked this video')
                    return redirect(sourceurl)
                else:
                    Like.objects.filter(username=username, videotitle=videotitle).delete()
                    messages.success(request, 'You Unliked this video')
                    return redirect(sourceurl)
    else:
        return redirect('index')
def video(request, videotitle):
    print('Video Title:',videotitle)
    #videos = Video.objects.all().filter(uploader=request.user.username)
    videos = Video.objects.all()
    videonow = Video.objects.get(title=videotitle)
    videourl = videonow.video.url
    videonowtitle = videonow.title
    videonowdescription = videonow.description
    likes = Like.objects.all().filter(username=request.user.username)
    videotitles = []
    for like in likes:
        if like.username == request.user.username:
            title = str(like.videotitle)
            videotitles.append(title)
    print('Videotitles',videotitles)
    context = {
        'videos': videos,
        'videonow': videonow,
        'videourl': videourl,
        'videonowtitle': videonowtitle,
        'videonowdescription': videonowdescription,
    }
    return render(request,'videos/video.html', context)
def search(request):
    queryset_list = Video.objects.all()
    if 'searchquery' in request.GET:
        searchquery = request.GET['searchquery']
        if searchquery:
            videos = queryset_list.filter(title__icontains=searchquery)
            print('Search Videos Title:',videos)
        else:
            showblankmessage = True
            context = {
                'showblankmessage': showblankmessage,
            }
            return render(request, 'videos/search.html', context)
        if request.user.is_authenticated:
            likes = Like.objects.all()
            videotitles = []
            for like in likes:
                if like.username == request.user.username:
                    title = str(like.videotitle)
                    videotitles.append(title)
            context = {
                'likes': likes,
                'videotitles': videotitles,
                'videos': videos
            }
        else:
            context = {
                'videos': videos
            }
        return render(request, 'videos/search.html', context)
def videosettings(request, videotitle):
    if request.user.is_authenticated:
        video = Video.objects.get(title=videotitle)
        currentitle = video.title
        videouploader = video.uploader
        context = {
            'currentitle': currentitle,
            'videouploader': videouploader
        }
        return render(request,'videos/videosettings.html', context)
    else:
        return redirect('index')
def videoupdate(request):
    if request.method == 'POST':
        currentitle = request.POST['currentitle']
        videouploader = request.POST['videouploader']
        newtitle = request.POST['newtitle']
        newdescription = request.POST['newdescription']
        newthumbnail = request.FILES['newthumbnail']
        if videouploader == request.user.username:
            if Like.objects.filter(videotitle=currentitle).exists():
                likes = Like.objects.filter(videotitle=currentitle)
                for like in likes:
                    like.videotitle = newtitle
                    like.save()
            if Video.objects.filter(title=currentitle).exists():
                target = Video.objects.get(title=currentitle)
                target.title = newtitle
                target.description = newdescription
                target.thumbnail = newthumbnail
                target.save()
                messages.success(request, 'Your video has been updated')
                return redirect('dashboard')
        else:
            messages.error(request,'You do not own this content')
            return redirect('index')
    else:
        return redirect('index')
def videodelete(request, videotitle):
    if request.method == 'POST':
        if Video.objects.filter(title=videotitle).exists():
            video = Video.objects.get(title=videotitle)
            video.delete()
            messages.success(request,'Your video has been deleted')
            return redirect('dashboard')
    else:
        return redirect('index')
