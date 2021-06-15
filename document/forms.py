from django import forms
from document.models import DocumentChat

class DocumentChatForm(forms.ModelForm):
    meeting_id = forms.IntegerField()
    class Meta:
        model = DocumentChat
        fields = ('name', 'file')