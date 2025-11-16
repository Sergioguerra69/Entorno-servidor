
import json
from channels.generic.websocket import WebsocketConsumer

class GameConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        game_data = json.loads(text_data)
        
        # Now the game logic should be here!
        # You should still save things to the database to allow
        # persistance. You can modify game_data (a dictionary) and then
        # save it to the db.
        # PS: Add game logic here means delete it from your views.py :D
        
        # Once the logic is done, send the updated game to the listeners
        self.send(text_data=json.dumps(game_data))