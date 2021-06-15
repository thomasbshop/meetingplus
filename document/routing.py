from django.urls import re_path, path
from . import consumers
from django.core.asgi import get_asgi_application

websocket_urlpatterns = [
    re_path(r'ws/meeting/document/(?P<document_id>\w+)/$', 
    consumers.DocumentChatConsumer.as_asgi()),
]