from django.urls import path
from . import views

urlpatterns = [
    path('universes/', views.universe_list, name='universe_list'),
    path('universes/new/', views.universe_create, name='universe_create'),
    path('universes/<int:universe_id>/', views.universe_detail, name='universe_detail'),
    path('universes/<int:universe_id>/characters/new/', views.character_create, name='character_create'),
]