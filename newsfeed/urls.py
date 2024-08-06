from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from .views import index, ArticleListView, ArticleDetailView

from django.conf import settings

app_name = 'newsfeed'

urlpatterns = [
    path('feed/', ArticleListView.as_view(), name='base'),
    path('feed/article_<int:pk>/', ArticleDetailView.as_view(), name='article-detail')
]
