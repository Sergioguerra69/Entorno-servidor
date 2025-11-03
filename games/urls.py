from django.urls import path
from . import views

app_name = 'games'

urlpatterns = [
    path('', views.lista_juegos, name='lista_juegos'),
    path('home/', views.home_games, name='home_games'),
    path('juego/<str:nombre_sala>/', views.detalle_juego, name='detalle_juego'),
]