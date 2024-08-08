import os

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.files.images import get_image_dimensions
from django.http import HttpRequest, HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy

from News_Quest.settings import BASE_DIR
from newsfeed.models import Article


def login_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse_lazy('newsfeed:base'))

    error_message = None

    if request.method == 'POST':
        username_or_email = request.POST.get('username')
        password = request.POST.get('password')

        if '@' in username_or_email:
            try:
                user = User.objects.get(email=username_or_email)
                username = user.username
            except User.DoesNotExist:
                username = None
        else:
            username = username_or_email

        usr = authenticate(request, username=username, password=password)
        if usr is not None:
            login(request, usr)
            return HttpResponseRedirect(reverse_lazy('newsfeed:base'))
        else:
            error_message = 'Invalid credentials'

    return render(request, 'siteauth/login.html', {'error': error_message})


def register_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse_lazy('newsfeed:base'))

    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        email = request.POST.get('email')

        if password1 == password2:
            if not User.objects.filter(username=username).exists():
                User.objects.create_user(username, email, password1)
                usr = authenticate(request, username=username, password=password1)

                if usr is not None:
                    login(request, usr)
                    return HttpResponseRedirect(reverse_lazy('newsfeed:base'))
                else:
                    return render(request, 'siteauth/login.html', {'error': 'Authentication failed'})
            else:
                return render(request, 'siteauth/register.html', {'error': 'Username already exists'})
        else:
            return render(request, 'siteauth/register.html', {'error': 'Passwords do not match'})

    return render(request, 'siteauth/register.html')


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('newsfeed:base')
    return render(request, 'siteauth/logout.html')


@login_required(login_url=reverse_lazy('siteauth:login'))
def profile_view(request: HttpRequest, username) -> HttpResponse:
    if request.method == 'POST':
        avatar = request.FILES.get('user_avatar')  # Получаем новую аватарку
        if avatar:
            try:
                # Проверка типа файла
                if not avatar.content_type.startswith('image/'):
                    raise ValueError("Файл должен быть изображением")

                # Проверка размера файла
                if avatar.size > 5 * 1024 * 1024:
                    raise ValueError("Размер изображения не должен превышать 5MB")

                # Проверка разрешения изображения
                width, height = get_image_dimensions(avatar)
                if width > 768 or height > 768:
                    raise ValueError("Разрешение изображения не должно превышать 768x768 пикселей")

                # Сохраняем новый аватар
                profile = request.user.profile
                if profile.user_avatar and profile.user_avatar.url != '/static/uploads/users/avatars/blank_avatar.png':
                    profile.user_avatar.delete(save=False)
                profile.user_avatar = avatar
                profile.save()

            except (IOError, ValueError) as e:
                # Логирование ошибок
                return render(request, 'siteauth/about_me.html', {
                    'user': request.user,
                    'error': str(e)
                })
        else:
            # Обработать случай, когда пользователь не загрузил новую аватарку
            return render(request, 'siteauth/about_me.html', {
                'user': request.user,
                'error': "Вы не загрузили изображение"
            })

    user = get_object_or_404(
        User.objects.prefetch_related('profile'),
        username=username
    )
    articles = Article.objects.filter(published_by=user)
    context = {
        'articles': articles,
        'user': user
    }
    return render(request, 'siteauth/about_me.html', context)


@login_required(login_url=reverse_lazy('siteauth:login'))
def reset_avatar_view(request, username):
    if request.method == 'POST' and request.user.username == username:
        blank_avatar_path = os.path.join(BASE_DIR, 'uploads\\users\\avatars\\blank_avatar.png')
        print('ПУТЬ ДО ПУСТОГО АВАТАРА', blank_avatar_path)
        profile = request.user.profile

        if profile.user_avatar and profile.user_avatar.path != blank_avatar_path:
            current_avatar_path = profile.user_avatar.path
            profile.user_avatar = blank_avatar_path
            profile.save()
            print('АВАТАР УДАЛЕН', current_avatar_path)
            os.remove(current_avatar_path)  # Удаляем файл вручную

        return redirect('siteauth:about_me', username=username)

    return redirect('siteauth:about_me', username=username)
