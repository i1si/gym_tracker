from django.contrib.auth import logout
from django.shortcuts import redirect, render

from main.models import Training


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


def trainings_view(request):
    if request.user.is_authenticated:
        success = request.GET.get('f', None)
        return render(request, 'main/trainings.html', {'success': success})
    return redirect('login')


def training_view(request, training_id):
    training = Training.objects.get(pk=training_id)
    if request.user == training.owner:
        return render(request, 'main/training.html', {'training': training})
    return redirect('trainings')
