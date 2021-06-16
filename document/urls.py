from django.urls import path
from .views import document, document_messages

urlpatterns = [
    path(r"document/<int:document_id>/", document, name="document"),
    path(r"document/messages/<int:document_id>/", document_messages),
]