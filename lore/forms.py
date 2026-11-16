from django import forms
from .models import Universe, Character

class UniverseForm(forms.ModelForm):
    class Meta:
        model = Universe
        fields = ['name', 'description']

class CharacterForm(forms.ModelForm):
    class Meta:
        model = Character
        fields = ['name', 'aliases', 'role', 'description']