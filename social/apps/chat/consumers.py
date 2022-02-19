import json

from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

#from .models import *
from user.models import User

@sync_to_async
def MarkMSeen(user, partner):
	#m = Message.objects.filter(receiver=User.objects.get(pk=user), sender=User.objects.get(pk=partner), is_seen = False)
	# m = None
	# if m:
	# 	for ms in m:
	# 		ms.is_seen = True
	return True

class ChatConsumer(AsyncWebsocketConsumer):
	async def connect(self):
		self.userID = self.scope['user'].id
		self.partnerID = self.scope['url_route']['kwargs']['partner']
		self.room_group_name = str('chat_{0}_with_{1}'.format(self.userID, self.partnerID))
		await self.channel_layer.group_add(
			self.room_group_name,
			self.channel_name
		)

		await self.accept()
		#await MarkMSeen(self.userID, self.partnerID)
	async def disconnect(self, close_code):
		# Leave room
		await self.channel_layer.group_discard(
			self.room_group_name,
			self.channel_name
		)
	
	async def receive(self, text_data):

		data = json.loads(text_data)
		# pk = data.get('pk')
		# data.pop('pk')
		data['type'] = "chat_message"		
		# Send message to room group
		await self.channel_layer.group_send(self.room_group_name,data)

	# Receive message from room group
	async def chat_message(self, event):
		await self.send(text_data=json.dumps(event))


class GeneralMobileChatConsumer(AsyncWebsocketConsumer):
	async def connect(self):
		self.userID = self.scope['user'].id
		self.room_group_name = str('general_mobile_chat_{0}'.format(self.userID))
		await self.channel_layer.group_add(
			self.room_group_name,
			self.channel_name
		)
		await self.accept()

		# await self.channel_layer.group_send(self.room_group_name, {
		# 	'type' : "chat_message",
		# 	'welcome': "sb7"
		# })
	
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


class MobileChatConsumer(AsyncWebsocketConsumer):
	async def connect(self):
		self.userID = self.scope['user'].id
		self.partnerID = self.scope['url_route']['kwargs']['partner']
		self.room_group_name = str('mobile_chat_{0}_{1}'.format(self.userID, self.partnerID))
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