from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages, auth
from django.contrib.auth import authenticate, login, logout
from videos.models import Video, Like
from accounts.forms import UserUpdateForm
from accounts.models import EmailVerification
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import hashlib
import uuid

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'Login successful')
            User.is_authenticated=True
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login')
    else:
        return render(request, 'accounts/login.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        requestid = uuid.uuid4()
        purpose = 'userregistration'
        password2 = request.POST['password2']
        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email id already registered')
                return redirect('signup')
            else:
                if User.objects.filter(username=username).exists():
                    messages.error(request, 'Username already exists')
                    return redirect('signup')
                else:
                    user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password=password)
                    user.save()
                    messages.success(request, 'User successfully registered')
                    return redirect('login')
        else:
            messages.error(request, 'The passwords do not match')
            return redirect('signup')
    else:
        return render(request, 'accounts/signup.html')

def dashboard(request):
    if request.user.is_authenticated:
        videos = Video.objects.all().filter(uploader=request.user.username)
        likes = Like.objects.all().filter(username=request.user.username)
        likedvideos = Video.objects.all()
        videotitles = []
        for like in likes:
            if like.username == request.user.username:
                title = str(like.videotitle)
                videotitles.append(title)
        context = {
            'videos': videos,
            'likes': likes,
            'videotitles': videotitles,
            'likedvideos': likedvideos
        }
        return render(request, 'accounts/dashboard.html', context)
    else:
        return redirect('login')

def likes(request):
    if request.user.is_authenticated:
        likes = Like.objects.all().filter(username=request.user.username)
        likedvideos = Video.objects.all()
        videotitles = []
        for like in likes:
            if like.username == request.user.username:
                title = str(like.videotitle)
                videotitles.append(title)
        print('Videotitles', videotitles)
        context = {
            'likes': likes,
            'videotitles': videotitles,
            'likedvideos': likedvideos
        }
        return render(request, 'accounts/likes.html', context)
    else:
        return redirect('login')

def logout(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            auth.logout(request)
            messages.success(request, 'You have been successfully logged out')
            return redirect('index')
        else:
            return redirect('login')

def usersettings(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            userid = request.user.id
            username = request.POST['username']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            password = request.POST['password']
            password2 = request.POST['password2']
            form = UserUpdateForm(request.POST)
            if password == password2:
                if Video.objects.filter(uploader=request.user.username).exists():
                    queryset1 = Video.objects.filter(uploader=request.user.username)
                    for queryitem1 in queryset1:
                        queryitem1.uploader = username
                        queryitem1.save()
                if Like.objects.filter(username=request.user.username).exists():
                    queryset2 = Like.objects.filter(username=request.user.username)
                    for queryitems2 in queryset2:
                        queryitems2.username = username
                        queryitems2.save()
                if User.objects.filter(id=userid).exists():
                    query = User(id=userid,username=username,first_name=first_name,last_name=last_name,email=email)
                    query.save()
                    userobj = User.objects.get(id=userid)
                    userobj.set_password(password)
                    userobj.save()
                    messages.success(request,'Updated your information')
                    return redirect('usersettings')
                else:
                    messages.error(request,'Invalid Input')
                    return redirect('usersettings')
            else:
                messages.error(request,'Passwords do not match')
                return redirect('usersettings')
        else:
            return render(request,'accounts/usersettings.html')
    else:
        return redirect('login')

def userdelete(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            if Like.objects.filter(username=request.user.username).exists():
                userlikes = Like.objects.filter(username=request.user.username)
                for userlike in userlikes:
                    userlike.delete()
            if Video.objects.filter(uploader=request.user.username).exists():
                uservideos = Video.objects.filter(uploader=request.user.username)
                for uservideo in uservideos:
                    uservideo.delete()
            if User.objects.filter(username=request.user.username).exists():
                user = User.objects.get(username=request.user.username)
                user.delete()
                messages.success(request, 'You have successfully deleted your account')
                return redirect('index')
    else:
        return redirect('login')

def passwordreset(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        purpose = request.POST['purpose']
        requestid = uuid.uuid4()
        from_email = "shivayf22@gmail.com"
        subject = "Password Reset"
        recipient_list = [ email ]
        if User.objects.filter(username=username, email=email).exists():
            if EmailVerification.objects.filter(username=username, email=email, purpose=purpose).exists():
                query1 = EmailVerification.objects.get(username=username, email=email, purpose=purpose)
                query1.delete()
                query2 = EmailVerification(username=username,email=email, requestid=requestid, purpose=purpose)
                query2.save()
                context = {
                 'requestid': requestid
                }
                html_message = render_to_string('accounts/email_verification_template.html', context)
                message = strip_tags(html_message)
                send_mail(subject, message, from_email, recipient_list, fail_silently=False,html_message=html_message)
                messages.success(request, 'A verification email has sent to you registered email id')
                return redirect('emailverificationform')
            else:
                query = EmailVerification(username=username,email=email, requestid=requestid, purpose=purpose)
                query.save()
                context = {
                 'requestid': requestid
                }
                html_message = render_to_string('accounts/email_verification_template.html', context)
                message = strip_tags(html_message)
                send_mail(subject, message, from_email, recipient_list, fail_silently=False, html_message=html_message)
                messages.success(request, 'A verification email has sent to you registered email id')
                return redirect('emailverificationform')
        else:
            text = 'Your credentials are invalid'
        context = {
            'text': text
        }
        return render(request, 'accounts/forgotpassword.html',context)
    else:
        return render(request, 'accounts/forgotpassword.html')
def emailverificationform(request):
    if request.method == 'POST':
        verificationid = request.POST['verificationid']
        if EmailVerification.objects.filter(requestid=verificationid).exists():
            queryvalue = EmailVerification.objects.get(requestid=verificationid)
            if queryvalue.requestid == verificationid:
                context = {
                 'verificationid': verificationid,
                }
                messages.success(request, 'Email Verification successfull')
                return render(request, 'accounts/reset_password.html', context)
            else:
                messages.error(request, 'Email verification failed')
                return render(request, 'accounts/email_verification_form.html')
    else:
        return render(request, 'accounts/email_verification_form.html')

def reset_password(request):
    if request.method == 'POST':
        newpassword = request.POST['password']
        newpassword2 = request.POST['password2']
        verificationid = request.POST['verificationid']
        query_source = EmailVerification.objects.get(requestid=verificationid)
        username = query_source.username
        if newpassword == newpassword2:
            query_select = User.objects.get(username=username)
            query_select.set_password(newpassword)
            query_select.save()
            query_source.delete()
            messages.success(request, 'Password reset successfull')
            return redirect('login')
        else:
            messages.error(request, 'Passwords do not match')
