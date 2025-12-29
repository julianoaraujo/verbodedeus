from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UsuarioRegistrationForm, UsuarioUpdateForm
from .models import Usuario


def register(request):
    if request.method == 'POST':
        form = UsuarioRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Cadastro realizado com sucesso!')
            return redirect('home')
    else:
        form = UsuarioRegistrationForm()
    return render(request, 'usuarios/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        form = UsuarioUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil atualizado com sucesso!')
            return redirect('profile')
    else:
        form = UsuarioUpdateForm(instance=request.user)
    return render(request, 'usuarios/profile.html', {'form': form})


def home(request):
    return render(request, 'home.html')

