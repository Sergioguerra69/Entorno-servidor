from django.db import models
import os
from django.db import models
from django.contrib.auth.models import User


def user_directory_path(instance, filename):
    return 'personas/person_{0}/{1}'.format(instance.slug, filename)

class Person(models.Model):
    name = models.CharField(max_length=50)
    birth = models.DateField()
    slug = models.SlugField(unique=True)
    mail = models.CharField(max_length=100, default='')
    propic = models.ImageField(
        upload_to=user_directory_path, 
        default='users/default_user.png',
        blank=True
    )
    
    def __str__(self):
        return self.name


class Profile(models.Model):
    person = models.OneToOneField(Person, on_delete=models.CASCADE)
    bio = models.TextField()
    website = models.URLField(blank=True)
    
    def __str__(self):
        return f"Profile of {self.person.name}"


class Product(models.Model):
    CASAS = [
        ('CAS', 'Casa'),
        ('APA', 'Apartamento'),
        ('TER', 'Terreno'),
    ]
    
    name = models.CharField(max_length=100)
    price = models.FloatField()
    description = models.TextField()
    category = models.CharField(max_length=3, choices=CASAS)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_published = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}, por {self.user.username}"