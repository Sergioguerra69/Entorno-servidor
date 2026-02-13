from django.shortcuts import render
import requests

def obtener_chiste(request):
    # voy a buscar un chiste a internet
    url = "https://official-joke-api.appspot.com/random_joke"
    
    try:
        # le pido el chiste a la API
        respuesta = requests.get(url)
        
        # si la API responde bien (200 = todo ok)
        if respuesta.status_code == 200:
            chiste = respuesta.json()  # convierto a formato python
            tiene_error = False
        else:
            # la API respondio pero con error
            chiste = {}
            tiene_error = True
            
    except:
        # no se pudo conectar con la API 
        chiste = {}
        tiene_error = True
    
    # envio el chiste al template
    return render(request, 'chistes/chiste.html', {
        'chiste': chiste,
        'tiene_error': tiene_error
    })