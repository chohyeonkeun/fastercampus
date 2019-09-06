from django.urls import path

from django.contrib.auth.views import LoginView, LogoutView

from .views import *

app_name = "accounts"

urlpatterns = [
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('signup/', user_signup, name='signup'),
]