from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Universe
from .forms import UniverseForm

# Create your views here.

@login_required
def universe_list(request):
    """READ: Displays only the Universes owned by the logged-in user."""
    universes = Universe.objects.filter(creator=request.user).order_by('-created_at')
    return render(request, 'lore/universe_list.html', {'universes': universes})

@login_required
def universe_create(request):
    """CREATE: Validates input and assigns the logged-in user as the creator."""
    if request.method == 'POST':
        form = UniverseForm(request.POST)
        if form.is_valid():
            universe = form.save(commit=False)
            universe.creator = request.user # Automatically assign the creator
            universe.save()
            messages.success(request, f"Universe '{universe.name}' created successfully!")
            return redirect('universe_list')
        else:
            messages.error(request, "Failed to create Universe. Please check the form.")
    else:
        form = UniverseForm()
    
    return render(request, 'lore/universe_form.html', {'form': form})