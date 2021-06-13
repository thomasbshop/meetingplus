from django.urls import path
from . import views

app_name = 'meeting_room'

urlpatterns = [
    # path('room/<int:meeting_id>/', views.meeting_chat_room, name='meeting_chat_room'),
    path('chat/<int:meeting_id>/', views.meeting_chat_room, name='meeting_chat_room'),
    path('room/<str:room_name>/', views.room, name='room'),
]