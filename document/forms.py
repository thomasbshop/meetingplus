from django.forms import ModelForm
from document.models import DocumentChat

class DocumentChatForm(ModelForm):
    class Meta:
        model = DocumentChat
        fields = ('name', 'file')