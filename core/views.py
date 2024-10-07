from django.shortcuts import render,redirect
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegistrationForm,ProfileForm
from .models import Profile
from django.contrib.auth.decorators import login_required

def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('profile')  # Redirect to the dashboard after login
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to the login page after successful registration
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})


@login_required
def profile(request):
    profile = request.user.profile  # Access the logged-in user's profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('dashboard')  # Redirect to the dashboard after saving profile
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'profile.html', {'form': form})