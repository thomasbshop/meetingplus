from django.conf.urls import url
from django.urls import path
from meeting_room.views import minutes, agenda

urlpatterns = [
    # path("", dashboard, name="dashboard"),
    path(r"agenda", agenda, name="agenda"),
    path(r"minutes/", minutes, name="minutes"),
]