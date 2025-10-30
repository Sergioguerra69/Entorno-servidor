from django.contrib import admin
from .models import Person, Profile

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'birth', 'slug', 'mail')
    list_filter = ('birth',)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('person', 'website')



