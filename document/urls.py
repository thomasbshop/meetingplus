from django.urls import path
from .views import document

urlpatterns = [
    path(r"document/<int:document_id>/", document, name="document"),
]