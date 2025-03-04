from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Note

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'file', 'category', 'tags', 'year', 'semester', 'subject']
