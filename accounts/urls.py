from django.urls import path
from . import views
urlpatterns = [
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/likes', views.likes, name='likes'),
    path('logout/', views.logout, name='logout'),
    path('usersettings', views.usersettings, name='usersettings'),
    path('userdelete', views.userdelete, name='userdelete'),
    path('passwordreset',views.passwordreset, name='passwordreset'),
    path('emailverificationform',views.emailverificationform, name='emailverificationform'),
    path('reset_password', views.reset_password, name='reset_password')
]
