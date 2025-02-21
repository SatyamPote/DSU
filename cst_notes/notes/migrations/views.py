from django.shortcuts import render
from .models import Note

def home(request):
    return render(request, 'home.html')

def notes(request):
    subjects = {
        'DSA': 'Data Structures & Algorithms',
        'OS': 'Operating Systems',
        'DBMS': 'Database Management Systems',
        'CN': 'Computer Networks',
        'AI': 'Artificial Intelligence',
    }
    notes_by_subject = {subject: Note.objects.filter(subject=code) for code, subject in subjects.items()}
    
    return render(request, 'notes.html', {'notes_by_subject': notes_by_subject})
