from django.urls import path
from . import views

app_name = 'productos'

urlpatterns = [
    path('lista/', views.lista_productos_view, name='lista'),
]