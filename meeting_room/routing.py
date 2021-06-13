from django.urls import re_path, path
from . import consumers
from django.core.asgi import get_asgi_application

websocket_urlpatterns = [
    re_path(r'ws/meeting/room/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
    re_path(r'ws/meeting/chat/(?P<meeting_id>\w+)/$', consumers.MeetingChatConsumer.as_asgi()),
]