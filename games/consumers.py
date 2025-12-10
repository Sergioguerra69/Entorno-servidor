import json
import re
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from .models import Juego

class TicTacToeConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        if self.scope["user"] == AnonymousUser():
            await self.close()
            return

        self.nombre_sala = self.scope['url_route']['kwargs']['nombre_sala']
        self.room_group_name = self.sanitize_group_name(f'tictactoe_{self.nombre_sala}')
        self.usuario = self.scope["user"]

        juego_existe = await self.verificar_juego_existe()
        if not juego_existe:
            await self.close()
            return

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        juego_data = await self.get_juego_data()
        if juego_data:
            await self.send(text_data=json.dumps({
                'type': 'game_state',
                'data': juego_data
            }))

    def sanitize_group_name(self, name):
        sanitized = re.sub(r'[^\w\.\-]', '_', name)
        return sanitized[:99]

    async def disconnect(self, close_code):
        if hasattr(self, 'room_group_name'):
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            message_type = data.get('type')
            
            if message_type == 'make_move':
                await self.procesar_movimiento(data)
                
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({
                'error': 'Mensaje inválido'
            }))

    async def procesar_movimiento(self, data):
        posicion = data.get('position')
        
        if posicion is None:
            await self.send(text_data=json.dumps({
                'error': 'Posición no especificada'
            }))
            return

        movimiento_exitoso, mensaje = await self.realizar_movimiento_bd(posicion)
        
        if movimiento_exitoso:
            juego_data = await self.get_juego_data()
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'game_update',
                    'data': juego_data,
                }
            )
        else:
            await self.send(text_data=json.dumps({
                'error': mensaje
            }))

    async def game_update(self, event):
        await self.send(text_data=json.dumps({
            'type': 'game_update',
            'data': event['data'],
        }))

    @database_sync_to_async
    def verificar_juego_existe(self):
        return Juego.objects.filter(nombre_sala=self.nombre_sala).exists()

    @database_sync_to_async
    def get_juego_data(self):
        try:
            juego = Juego.objects.get(nombre_sala=self.nombre_sala)
            return {
                'tablero': juego.obtener_tablero_array(),
                'jugador_actual': juego.jugador_actual,
                'estado_juego': juego.estado_juego,
                'propietario': juego.propietario.username,
                'jugador_o': juego.jugador_o.username if juego.jugador_o else None,
                'ganador': self.determinar_ganador(juego.estado_juego),
                'puede_jugar': self.puede_jugar(juego)
            }
        except Juego.DoesNotExist:
            return None

    @database_sync_to_async
    def realizar_movimiento_bd(self, posicion):
        try:
            juego = Juego.objects.get(nombre_sala=self.nombre_sala)
            
            print(f"DEBUG: Usuario {self.usuario.username} intentando mover en posición {posicion}")
            print(f"DEBUG: Estado juego: {juego.estado_juego}")
            print(f"DEBUG: Jugador actual: {juego.jugador_actual}")
            print(f"DEBUG: Propietario: {juego.propietario.username}")
            print(f"DEBUG: Jugador O: {juego.jugador_o.username if juego.jugador_o else 'None'}")
            
            if juego.estado_juego != 'ACTIVO':
                return False, 'El juego ya terminó'
            
            if posicion < 0 or posicion > 8:
                return False, 'Posición inválida (debe ser 0-8)'
            
            if juego.realizar_movimiento(int(posicion), self.usuario):
                return True, 'Movimiento exitoso'
            else:
                return False, 'Movimiento inválido - no es tu turno o casilla ocupada'
                
        except Juego.DoesNotExist:
            return False, 'Juego no encontrado'
        except Exception as e:
            return False, f'Error: {str(e)}'

    def determinar_ganador(self, estado):
        if estado == 'X_GANO':
            return 'X'
        elif estado == 'O_GANO':
            return 'O'
        elif estado == 'EMPATE':
            return 'Empate'
        return None

    def puede_jugar(self, juego):
        if juego.estado_juego != 'ACTIVO':
            return False
        
        if self.usuario.username == juego.propietario.username and juego.jugador_actual == 'X':
            return True
        if juego.jugador_o and self.usuario.username == juego.jugador_o.username and juego.jugador_actual == 'O':
            return True
            
        return False