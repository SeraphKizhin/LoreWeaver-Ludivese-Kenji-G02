from django.urls import path
from . import views

urlpatterns = [
    path('universes/', views.universe_list, name='universe_list'),
    path('universes/new/', views.universe_create, name='universe_create'),
]