from django.shortcuts import render, get_object_or_404
from .models import Person

def homepage(request):
    person_list = Person.objects.all()
    return render(request, 'miproyecto/hom3.html', {'persons': person_list})

def person_detail(request, slug):
    person = get_object_or_404(Person, slug=slug)
    return render(request, 'miproyecto/person.html', {'person': person})