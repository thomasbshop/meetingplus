from django import forms

class DocumentForm(forms.ModelForm):
    name = forms.CharField(label='Document name...', max_length=100)
    document = forms.FileField()