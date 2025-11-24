from django.urls import path
from . import views

urlpatterns = [
    path('status/', views.get_server_status, name='server_status'),
    path('errors/', views.get_errors, name='get_errors'),
    path('errors/create/', views.create_error, name='create_error'),
    path('error/<int:code>/', views.get_error_from_code, name='error_by_code'),
    path('error/update/<int:id>/', views.error_update, name='error_update'),
]