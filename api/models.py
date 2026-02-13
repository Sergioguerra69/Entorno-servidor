from django.db import models

# Create your models here.
from django.db import models

class ErrorReport(models.Model):
    # que error paso 
    code = models.IntegerField()
    # que dice el error
    description = models.TextField()
    # cuando paso (se pone solo)
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        # como se ve cuando imprimes un error
        return f"Error {self.code}: {self.description[:50]}"
    
    class Meta:
        # los mas nuevos primero
        ordering = ['-date']