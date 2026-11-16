from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm, UserProfileForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

# Create your views here.

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect('dashboard_router')
        else:
            messages.error(request, "Registration failed. Please check the errors below.")
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                return redirect('dashboard_router')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('login')

def dashboard_view(request):
    return render(request, 'accounts/dashboard.html')

@login_required
def dashboard_router(request):
    """Routes the user to their specific dashboard based on their role."""
    if request.user.role == 'admin':
        return redirect('admin_dashboard')
    elif request.user.role == 'creator':
        return redirect('creator_dashboard')
    else:
        return redirect('login')

@login_required
def admin_dashboard_view(request):
    """Strictly protected dashboard for Admins."""
    if request.user.role != 'admin':
        raise PermissionDenied("You do not have permission to view the Admin dashboard.")
    return render(request, 'accounts/admin_dashboard.html')

@login_required
def creator_dashboard_view(request):
    """Strictly protected dashboard for Creators."""
    if request.user.role != 'creator':
        raise PermissionDenied("You do not have permission to view the Creator dashboard.")
    return render(request, 'accounts/creator_dashboard.html')

@login_required
def profile_view(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated!")
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)
        
    return render(request, 'accounts/profile.html', {'form': form})