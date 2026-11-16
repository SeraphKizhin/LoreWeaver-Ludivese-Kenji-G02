from django.db import models
from django.conf import settings

# Create your models here.

class Universe(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='universes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Character(models.Model):
    universe = models.ForeignKey(Universe, on_delete=models.CASCADE, related_name='characters')
    name = models.CharField(max_length=200)
    aliases = models.CharField(max_length=255, blank=True, null=True)
    role = models.CharField(max_length=100, blank=True, null=True, help_text="e.g., Protagonist, Antagonist, Supporting")
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name