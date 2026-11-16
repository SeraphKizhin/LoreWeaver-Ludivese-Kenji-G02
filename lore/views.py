from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Universe, Character
from .forms import UniverseForm, CharacterForm

# Create your views here.

def landing_page(request):
    """The public homepage for LoreWeaver."""
    if request.user.is_authenticated:
        return redirect('dashboard_router')
    return render(request, 'lore/landing.html')

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

@login_required
def universe_detail(request, universe_id):
    """READ: Displays the details of a Universe and its Characters."""
    universe = get_object_or_404(Universe, id=universe_id, creator=request.user)
    characters = universe.characters.all().order_by('-created_at')
    return render(request, 'lore/universe_detail.html', {'universe': universe, 'characters': characters})

@login_required
def character_create(request, universe_id):
    """CREATE: Adds a new character to a specific Universe."""
    universe = get_object_or_404(Universe, id=universe_id, creator=request.user)
    
    if request.method == 'POST':
        form = CharacterForm(request.POST)
        if form.is_valid():
            character = form.save(commit=False)
            character.universe = universe # Automatically assign the Universe
            character.save()
            messages.success(request, f"Character '{character.name}' added successfully!")
            return redirect('universe_detail', universe_id=universe.id)
    else:
        form = CharacterForm()
    
    return render(request, 'lore/character_form.html', {'form': form, 'universe': universe})