from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Juego
from .forms import JuegoForm  # El formulario se llama JuegoForm


def home_games(request):
    """Página de inicio de la app Games"""
    return render(request, 'games/home.html')


@login_required
def lista_juegos(request):
    """Lista de juegos activos Tic Tac Toe en la base de datos"""
    juegos_activos = Juego.objects.filter(estado_juego='ACTIVO')
    
    if request.method == 'POST':
        formulario = JuegoForm(request.POST)  # Cambia a JuegoForm
        if formulario.is_valid():
            juego = formulario.save(commit=False)
            juego.propietario = request.user
            juego.save()
            return redirect('games:detalle_juego', nombre_sala=juego.nombre_sala)
    else:
        formulario = JuegoForm()  # Cambia a JuegoForm
    
    return render(request, 'games/lista_juegos.html', {
        'juegos_activos': juegos_activos,
        'formulario': formulario,
        'user': request.user  # Añade esto para que el template funcione
    })


@login_required
def detalle_juego(request, nombre_sala):
    """Página que muestra el juego en su estado actual"""
    juego = get_object_or_404(Juego, nombre_sala=nombre_sala)
    
    # Lógica para POST request (como pide el ejercicio)
    if request.method == 'POST':
        # b. Retrieve the square selected by the user.
        if 'submit' in request.POST:
            posicion = int(request.POST.get('submit'))
            
            if request.user == juego.propietario and juego.estado_juego == 'ACTIVO':
                if juego.realizar_movimiento(posicion):
                    juego.save()
        
        elif 'eliminar' in request.POST and request.user == juego.propietario:
            juego.delete()
            return redirect('games:lista_juegos')
    
    tablero_array = juego.obtener_tablero_array()
    es_propietario = request.user == juego.propietario
    
    return render(request, 'games/detalle_juego.html', {
        'juego': juego,
        'tablero_array': tablero_array,
        'es_propietario': es_propietario,
        'user': request.user  # Añade esto también
    })