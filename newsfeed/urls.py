from django.urls import path

from .views import ArticleListView, ArticleDetailView, ArticleCreateView, ArticleLike

app_name = 'newsfeed'

urlpatterns = [
    path('feed/', ArticleListView.as_view(), name='base'),
    path('feed/article/create', ArticleCreateView.as_view(), name='article-create'),
    path('feed/article_<int:pk>/', ArticleDetailView.as_view(), name='article-detail'), \
    path('article/<int:pk>/like/', ArticleLike, name='article-like'),
]
