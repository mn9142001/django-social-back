import json

from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

class GeneralConsumer(AsyncWebsocketConsumer):
	async def connect(self):
		self.userID = self.scope['user'].id
		self.room_group_name = str('general_{0}'.format(self.userID))
		await self.channel_layer.group_add(
			self.room_group_name,
			self.channel_name
		)

		await self.accept()
	async def disconnect(self, close_code):
		await self.channel_layer.group_discard(
			self.room_group_name,
			self.channel_name
		)

	async def receive(self, text_data):
		data = json.loads(text_data)
		data['type'] = "chat_message"		
		await self.channel_layer.group_send(self.room_group_name,data)

	async def chat_message(self, event):
		await self.send(text_data=json.dumps(event))