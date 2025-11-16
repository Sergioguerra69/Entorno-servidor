from django.db import models
from django.contrib.auth.models import User

class Juego(models.Model):
    ESTADOS_JUEGO = [
        ('ACTIVO', 'Activo'),
        ('X_GANO', 'X Gano'),
        ('O_GANO', 'O Gano'),
        ('EMPATE', 'Empate'),
    ]
    
    nombre_sala = models.CharField(max_length=100, unique=True)  
    propietario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='juegos_como_x')  
    jugador_o = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='juegos_como_o')
    tablero = models.CharField(max_length=9, default=' ' * 9)    
    jugador_actual = models.CharField(max_length=1, default='X')  
    estado_juego = models.CharField(max_length=10, choices=ESTADOS_JUEGO, default='ACTIVO')  
    
    def __str__(self):
        return f"Juego: {self.nombre_sala}"
    
    def obtener_tablero_array(self):
        tablero_str = self.tablero
        return [
            [tablero_str[0], tablero_str[1], tablero_str[2]],
            [tablero_str[3], tablero_str[4], tablero_str[5]],
            [tablero_str[6], tablero_str[7], tablero_str[8]]
        ]
    
    def verificar_ganador(self):
        t = self.tablero
        for i in range(0, 9, 3):
            if t[i] != ' ' and t[i] == t[i+1] == t[i+2]:
                return t[i]
        for i in range(3):
            if t[i] != ' ' and t[i] == t[i+3] == t[i+6]:
                return t[i]
        if t[0] != ' ' and t[0] == t[4] == t[8]:
            return t[0]
        if t[2] != ' ' and t[2] == t[4] == t[6]:
            return t[2]
        return None
    
    def tablero_lleno(self):
        return ' ' not in self.tablero
    
    def realizar_movimiento(self, posicion, usuario_actual):
        if self.estado_juego != 'ACTIVO':
            return False
        
        if posicion < 0 or posicion >= 9:
            return False
        
        if self.tablero[posicion] != ' ':
            return False
        
        # Determinar que ficha corresponde al usuario
        if usuario_actual == self.propietario:
            ficha = 'X'
        elif self.jugador_o and usuario_actual == self.jugador_o:
            ficha = 'O'
        else:
            return False  # Usuario no es jugador de esta partida
        
        # Verificar que es el turno del usuario
        if self.jugador_actual != ficha:
            return False
        
        # Realizar el movimiento
        lista_tablero = list(self.tablero)
        lista_tablero[posicion] = ficha
        self.tablero = ''.join(lista_tablero)
        
        ganador = self.verificar_ganador()
        if ganador:
            self.estado_juego = 'X_GANO' if ganador == 'X' else 'O_GANO'
        elif self.tablero_lleno():
            self.estado_juego = 'EMPATE'
        else:
            self.jugador_actual = 'O' if self.jugador_actual == 'X' else 'X'
        
        self.save()
        return True