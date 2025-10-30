from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Producto

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'precio', 'categoria', 'usuario', 'fecha_publicacion']
    list_filter = ['categoria', 'fecha_publicacion']
    search_fields = ['nombre', 'descripcion']