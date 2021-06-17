from django import forms 

class AgendaForm(forms.Form):
    item = forms.CharField()