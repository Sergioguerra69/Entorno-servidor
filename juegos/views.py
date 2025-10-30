from django.shortcuts import render

# Create your views here.
def inicio_juegos(request):
    return render(request, 'juegos/juegos.html')
