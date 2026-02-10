
from django.shortcuts import render
import requests

def obtener_chiste(request):  
    url = "https://official-joke-api.appspot.com/random_joke"
    
    try:
        respuesta = requests.get(url)
        if respuesta.status_code == 200:
            chiste = respuesta.json()
            tiene_error = False
        else:
            chiste = {}
            tiene_error = True
    except:
        chiste = {}
        tiene_error = True
    
    return render(request, 'chistes/chiste.html', {
        'chiste': chiste,
        'tiene_error': tiene_error
    })