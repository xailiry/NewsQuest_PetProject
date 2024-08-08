from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpRequest
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView

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

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        likes_connected = get_object_or_404(Article, id=self.kwargs['pk'])
        liked = False
        if likes_connected.likes.filter(id=self.request.user.id).exists():
            liked = True
        data['number_of_likes'] = likes_connected.number_of_likes()
        data['post_is_liked'] = liked
        return data


@method_decorator(login_required(login_url=reverse_lazy('siteauth:login')), name='dispatch')
class ArticleCreateView(CreateView):
    model = Article
    template_name = 'newsfeed/article-create.html'
    fields = ['title', 'content', 'preview_img']

    def form_valid(self, form):
        form.instance.published_by = self.request.user
        return super().form_valid(form)



def ArticleLike(request, pk):
    post = get_object_or_404(Article, id=pk)
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True

    return JsonResponse({'likes': post.likes.count(), 'liked': liked})
