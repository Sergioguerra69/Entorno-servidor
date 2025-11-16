from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Juego  
from .forms import JuegoForm

def home_games(request):
    return render(request, 'games/home.html')

@login_required
def lista_juegos(request):
    juegos_activos = Juego.objects.filter(estado_juego='ACTIVO')
    
    if request.method == 'POST':
        formulario = JuegoForm(request.POST)
        if formulario.is_valid():
            juego = formulario.save(commit=False)
            juego.propietario = request.user
            juego.jugador_actual = 'X'
            juego.save()
            return redirect('games:detalle_juego', nombre_sala=juego.nombre_sala)
    else:
        formulario = JuegoForm()
    
    return render(request, 'games/lista_juegos.html', {
        'juegos_activos': juegos_activos,
        'formulario': formulario,
        'user': request.user
    })

@login_required
def detalle_juego(request, nombre_sala):
    juego = get_object_or_404(Juego, nombre_sala=nombre_sala)
    
    # Variables de estado CORREGIDAS
    es_jugador_x = request.user == juego.propietario
    es_jugador_o = juego.jugador_o and request.user == juego.jugador_o
    es_jugador_en_partida = es_jugador_x or es_jugador_o
    
    # Determinar si es el turno del usuario actual
    if es_jugador_x and juego.jugador_actual == 'X':
        es_turno_actual = True
    elif es_jugador_o and juego.jugador_actual == 'O':
        es_turno_actual = True
    else:
        es_turno_actual = False
    
    if request.method == 'POST':
        # UNIRSE COMO JUGADOR O
        if 'unirse' in request.POST and not es_jugador_en_partida and not juego.jugador_o:
            juego.jugador_o = request.user
            juego.save()
            return redirect('games:detalle_juego', nombre_sala=nombre_sala)
        
        # REALIZAR MOVIMIENTO
        elif 'submit' in request.POST and juego.estado_juego == 'ACTIVO':
            if es_jugador_en_partida and es_turno_actual:
                posicion = int(request.POST.get('submit'))
                
                # Usar el método corregido
                if juego.realizar_movimiento(posicion, request.user):
                    return redirect('games:detalle_juego', nombre_sala=nombre_sala)
        
        # ELIMINAR SALA
        elif 'eliminar' in request.POST and es_jugador_x:
            juego.delete()
            return redirect('games:lista_juegos')
    
    tablero_array = juego.obtener_tablero_array()
    
    # Determinar si el usuario puede unirse
    puede_unirse = (
        not es_jugador_en_partida and 
        not juego.jugador_o and 
        juego.estado_juego == 'ACTIVO'
    )
    
    # Determinar si el usuario puede jugar
    puede_jugar = (
        es_jugador_en_partida and 
        es_turno_actual and 
        juego.estado_juego == 'ACTIVO'
    )
    
    return render(request, 'games/detalle_juego.html', {
        'juego': juego,
        'tablero_array': tablero_array,
        'es_jugador_x': es_jugador_x,
        'es_jugador_o': es_jugador_o,
        'es_jugador_en_partida': es_jugador_en_partida,
        'es_turno_actual': es_turno_actual,
        'puede_jugar': puede_jugar,
        'puede_unirse': puede_unirse,
        'user': request.user
    })