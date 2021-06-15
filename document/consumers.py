from django.core.serializers.python import Serializer
from django.core.paginator import Paginator
from django.core.serializers import serialize
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.generic.websocket import WebsocketConsumer
from channels.db import database_sync_to_async
import json
from django.utils import timezone

from meeting_room.constants import *
from .models import DocumentChat, DocumentChatMessage
from meeting_room.exceptions import ClientError
from meeting_room.utils import calculate_timestamp

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        self.send(text_data=json.dumps({
            'message': message
        }))
        text_data_json = json.loads(text_data)
        message = text_data_json['message']


# Example taken from:
# https://github.com/andrewgodwin/channels-examples/blob/master/multichat/chat/consumers.py
class DocumentChatConsumer(AsyncJsonWebsocketConsumer):

	async def connect(self):
		"""
		Called when the websocket is handshaking as part of initial connection.
		"""
		print("MeetingChatConsumer: connect: " + str(self.scope["user"]))
		# let everyone connect. But limit read/write to authenticated users
		await self.accept()
		self.document_id = None

	async def disconnect(self, code):
		"""
		Called when the WebSocket closes for any reason.
		"""
		# leave the room
		print("MeetingChatConsumer: disconnect")
		try:
			if self.document_id != None:
				await self.leave_room(self.document_id)
		except Exception:
			pass

	async def receive_json(self, content):
		"""
		Called when we get a text frame. Channels will JSON-decode the payload
		for us and pass it as the first argument.
		"""
		# Messages will have a "command" key we can switch on
		command = content.get("command", None)
		print(f'MeetingChatConsumer: receive_json: { content["documentId"] }')
		try:
			if command == "send":
				if len(content["xfdfString"].lstrip()) != 0:
					await self.send_room(content["documentId"], content["xfdfString"])
					# raise ClientError(422,"You can't send an empty message.")
			elif command == "join":
				# Make them join the meeting
				await self.join_room(content["room"])
			elif command == "leave":
				# Leave the room
				await self.leave_room(content["room"])
			elif command == "get_room_chat_messages":
				await self.display_progress_bar(True)
				room = await get_room_or_error(content['document_id'])
				payload = await get_room_chat_messages(room, content['page_number'])
				if payload != None:
					payload = json.loads(payload)
					await self.send_messages_payload(payload['messages'], payload['new_page_number'])
				else:
					raise ClientError(204,"Something went wrong retrieving the chatroom messages.")
				await self.display_progress_bar(False)
		except ClientError as e:
			await self.display_progress_bar(False)
			await self.handle_client_error(e)

	async def send_room(self, document_id, message):
		"""
		Called by receive_json when someone sends a message to a document.
		"""
		# Check they are in this room
		print(f'MeetingChatConsumer: send_room {self.document_id }')
		if self.document_id != None:
			if str(document_id) != str(self.document_id):
				raise ClientError("ROOM_ACCESS_DENIED", "Room access denied")
			if not is_authenticated(self.scope["user"]):
				raise ClientError("AUTH_ERROR", "You must be authenticated to chat.")
		else:
			raise ClientError("ROOM_ACCESS_DENIED", "Room access denied")

		# Get the room and send to the group about it
		document = await get_room_or_error(document_id)
		print('docccccc', document)
		await create_meeting_room_chat_message(document, self.scope["user"], message)

		await self.channel_layer.group_send(
			document.group_name,
			{
				"type": "chat.message",
				# "profile_image": self.scope["user"].profile_image.url,
				"username": self.scope["user"].username,
				"user_id": self.scope["user"].id,
				"message": message,
			}
		)

	async def chat_message(self, event):
		"""
		Called when someone has messaged our chat.
		"""
		# Send a message down to the client
		print("MeetingChatConsumer: chat_message from user #" + str(event))
		timestamp = calculate_timestamp(timezone.now())
		await self.send_json(
			{
				# "msg_type": MSG_TYPE_MESSAGE,
				# # "username": event["username"],
				# "user_id": event["user_id"],
				# "message": event["message"],
				"natural_timestamp": timestamp,
			},
		)

	async def join_room(self, document_id):
		"""
		Called by receive_json when someone sent a join command.
		"""
		print("MeetingChatConsumer: join_room")
		is_auth = is_authenticated(self.scope["user"])
		try:
			room = await get_room_or_error(document_id)
		except ClientError as e:
			await self.handle_client_error(e)

		# Add user to "users" list for room
		if is_auth:
			await connect_user(room, self.scope["user"])

		# Store that we're in the room
		self.document_id = room.id

		# Add them to the group so they get room messages
		await self.channel_layer.group_add(
			room.group_name,
			self.channel_name,
		)

		# Instruct their client to finish opening the room
		await self.send_json({
			"join": str(room.id)
		})

		# send the new user count to the room
		num_connected_users = await get_num_connected_users(room)
		await self.channel_layer.group_send(
			room.group_name,
			{
				"type": "connected.user.count",
				"connected_user_count": num_connected_users,
			}
		)

	async def leave_room(self, document_id):
		"""
		Called by receive_json when someone sent a leave command.
		"""
		print("MeetingChatConsumer: leave_room")
		is_auth = is_authenticated(self.scope["user"])
		room = await get_room_or_error(document_id)

		# Remove user from "users" list
		if is_auth:
			await disconnect_user(room, self.scope["user"])

		# Remove that we're in the room
		self.document_id = None
		# Remove them from the group so they no longer get room messages
		await self.channel_layer.group_discard(
			room.group_name,
			self.channel_name,
		)

		# send the new user count to the room
		num_connected_users = get_num_connected_users(room)
		await self.channel_layer.group_send(
		room.group_name,
			{
				"type": "connected.user.count",
				"connected_user_count": num_connected_users,
			}
		)

	async def handle_client_error(self, e):
		"""
		Called when a ClientError is raised.
		Sends error data to UI.
		"""
		errorData = {}
		errorData['error'] = e.code
		if e.message:
			errorData['message'] = e.message
			await self.send_json(errorData)
		return

	async def send_messages_payload(self, messages, new_page_number):
		"""
		Send a payload of messages to the ui
		"""
		print("MeetingChatConsumer: send_messages_payload. ")

		await self.send_json(
			{
				"messages_payload": "messages_payload",
				"messages": messages,
				"new_page_number": new_page_number,
			},
		)

	async def connected_user_count(self, event):
		"""
		Called to send the number of connected users to the room.
		This number is displayed in the room so other users know how many users are connected to the chat.
		"""
		# Send a message down to the client
		print("MeetingChatConsumer: connected_user_count: count: " + str(event["connected_user_count"]))
		await self.send_json(
			{
				"msg_type": MSG_TYPE_CONNECTED_USER_COUNT,
				"connected_user_count": event["connected_user_count"]
			},
		)

	async def display_progress_bar(self, is_displayed):
		"""
		1. is_displayed = True
		- Display the progress bar on UI
		2. is_displayed = False
		- Hide the progress bar on UI
		"""
		print("DISPLAY PROGRESS BAR: " + str(is_displayed))
		await self.send_json(
			{
				"display_progress_bar": is_displayed
			}
		)


def is_authenticated(user):
	if user.is_authenticated:
		return True
	return False

@database_sync_to_async
def get_num_connected_users(room):
	if room.users:
		return len(room.users.all())
	return 0

@database_sync_to_async
def create_meeting_room_chat_message(document, user, message):
    return DocumentChatMessage.objects.create(user=user, document=document, content=message)

@database_sync_to_async
def connect_user(room, user):
    return room.connect_user(user)

@database_sync_to_async
def disconnect_user(room, user):
    return room.disconnect_user(user)

@database_sync_to_async
def get_room_or_error(document_id):
	"""
	Tries to fetch a document for the user
	"""
	try:
		print(document_id, '333333333333333333333333333333333333333333333333333333333333333')
		document = DocumentChat.objects.get(pk=document_id)
	except DocumentChat.DoesNotExist:
		raise ClientError("ROOM_INVALID", "Invalid room.")
	return document


@database_sync_to_async
def get_room_chat_messages(room, page_number):
	try:
		qs = DocumentChatMessage.objects.by_room(room)
		p = Paginator(qs, DEFAULT_ROOM_CHAT_MESSAGE_PAGE_SIZE)

		payload = {}
		messages_data = None
		new_page_number = int(page_number)  
		if new_page_number <= p.num_pages:
			new_page_number = new_page_number + 1
			s = LazyRoomChatMessageEncoder()
			payload['messages'] = s.serialize(p.page(page_number).object_list)
		else:
			payload['messages'] = "None"
		payload['new_page_number'] = new_page_number
		return json.dumps(payload)
	except Exception as e:
		print("EXCEPTION: " + str(e))
		return None



class LazyRoomChatMessageEncoder(Serializer):
	def get_dump_object(self, obj):
		dump_object = {}
		dump_object.update({'msg_type': MSG_TYPE_MESSAGE})
		dump_object.update({'msg_id': str(obj.id)})
		dump_object.update({'user_id': str(obj.user.id)})
		dump_object.update({'username': str(obj.user.username)})
		dump_object.update({'message': str(obj.content)})
		# dump_object.update({'profile_image': str(obj.user.profile_image.url)})
		dump_object.update({'natural_timestamp': calculate_timestamp(obj.timestamp)})
		return dump_object