from django.db import models

# Create your models here.
from django.db import models

class ErrorReport(models.Model):
    code = models.IntegerField()
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Error {self.code}: {self.description[:50]}"
    
    class Meta:
        ordering = ['-date']