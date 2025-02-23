from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Note  # Import the Note model

class StaffLoginForm(AuthenticationForm):
    pass  # Inherits default username and password fields

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'file', 'category', 'tags', 'year', 'semester', 'subject']