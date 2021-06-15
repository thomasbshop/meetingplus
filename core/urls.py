from django.conf.urls import url
from django.urls import path
from .views import dashboard, minutes

urlpatterns = [
    # path("", dashboard, name="dashboard"),
    # path(r"", dashboard, name="dashboard"),
    path(r"", minutes, name="minutes"),
]