from django.shortcuts import render
from django.http import HttpResponse
from .models import Note

def home(request):
    return render(request, 'home.html')

def notes(request):
    notes_list = Note.objects.all()
    return render(request, 'notes.html', {'notes': notes_list})
