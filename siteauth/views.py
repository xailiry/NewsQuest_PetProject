from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy


def login_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse_lazy('newsfeed:base'))

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        usr = authenticate(request, username=username, password=password)
        if usr is not None:
            login(request, usr)
            return HttpResponseRedirect(reverse_lazy('newsfeed:base'))
        else:
            return render(request, 'siteauth/login.html', {'error': 'Invalid credentials'})

    return render(request, 'siteauth/login.html')


def register_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse_lazy('newsfeed:base'))

    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password')
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