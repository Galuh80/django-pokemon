from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('pokemon/<str:name>/', views.pokemon_detail, name='pokemon_detail'),
    path('ability/<str:name>/', views.ability_detail, name='ability_detail'),
    path('gacha/', views.gacha, name='gacha'),
]