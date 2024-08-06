from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from django.views.generic import ListView, DetailView

from newsfeed.models import Article


def index(request: HttpRequest) -> HttpResponse:
    return render(request, 'newsfeed/base.html')


class ArticleListView(ListView):
    model = Article
    paginate_by = 20
    template_name = 'newsfeed/article-list.html'
    context_object_name = 'articles'


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'newsfeed/article-detail.html'
    context_object_name = 'article'
