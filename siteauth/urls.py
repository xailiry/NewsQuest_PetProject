from django.urls import path

from .views import register_view, login_view, logout_view, profile_view, reset_avatar_view

app_name = 'siteauth'

urlpatterns = [
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('profile/<str:username>/', profile_view, name='about_me'),
    path('profile/<str:username>/reset_avatar/', reset_avatar_view, name='reset_avatar'),
]
