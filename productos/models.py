from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Producto(models.Model):
    CASAS = [
        ('CAS', 'Casa'),
        ('APA', 'Apartamento'),
        ('TER', 'Terreno'),
    ]
    
    nombre = models.CharField(max_length=100)
    precio = models.FloatField()
    descripcion = models.TextField()
    categoria = models.CharField(max_length=3, choices=CASAS)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_publicacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre}, por {self.usuario.username}"