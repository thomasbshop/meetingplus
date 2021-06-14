from django.urls import path
from .views import meeting_chat_room, room, upload_file, upload_form

app_name = 'meeting_room'

urlpatterns = [
    # path('room/<int:meeting_id>/', views.meeting_chat_room, name='meeting_chat_room'),
    path('chat/<int:meeting_id>/', meeting_chat_room, name='meeting_chat_room'),
    path('room/<str:room_name>/', room, name='room'),
    path('upload_document/', upload_file, name='upload_file'),
    path('upload_form/', upload_form, name='upload_form'),
]