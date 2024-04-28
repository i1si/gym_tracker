from django.contrib.auth import logout
from django.shortcuts import redirect, render


def index_view(request):
    if request.user.is_authenticated:
        return redirect('progress')
    return render(request, 'main/index.html')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('progress')
    return render(request, 'main/register.html')


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('main')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('progress')
    return render(request, 'main/login.html')


def progress_view(request):
    if request.user.is_authenticated:
        return render(request, 'main/progress.html')
    return redirect('login')


def training_view(request):
    if request.user.is_authenticated:
        return render(request, 'main/training.html')
    return redirect('login')
