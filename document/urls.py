from django.urls import path
from .views import document

urlpatterns = [
    path(r"", document, name="document"),
]