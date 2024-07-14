import json
from channels.generic.websocket import WebsocketConsumer
import requests
# from channels.generic.websocket import AsyncWebsocketConsumer

class Consumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        # self.send(text_data="connect establish")

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        print(text_data)
        print("sending")
        res=requests.get("http://localhost:8000/api/newslist")
        self.send(res.content)
        print("sended")

    def send_nba_news(self, message):
        pass