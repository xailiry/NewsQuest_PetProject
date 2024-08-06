from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from django.conf import settings

from .views import register_view, login_view, logout_view

app_name = 'siteauth'

urlpatterns = [
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
]