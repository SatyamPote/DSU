from django.shortcuts import render, redirect, get_object_or_404
from .models import Note
from .forms import NoteForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

def home(request):
    return render(request, 'notes/home.html')

#@login_required  # Remove this line if you want everyone to see the notes
def notes_list(request):
    query = request.GET.get('q')
    if query:
        notes = Note.objects.filter(
            Q(title__icontains=query) | Q(category__icontains=query) | Q(tags__name__icontains=query)
        ).distinct()
    else:
        notes = Note.objects.all()
    return render(request, 'notes/notes.html', {'notes': notes, 'query': query})

@login_required
def note_upload(request):
    if request.method == 'POST':
        form = NoteForm(request.POST, request.FILES)
        if form.is_valid():
            note = form.save(commit=False)
            note.uploaded_by = request.user
            note.save()
            form.save_m2m()  # Save tags
            return redirect('notes')
    else:
        form = NoteForm()
    return render(request, 'notes/note_upload.html', {'form': form})

def download_note(request, note_id):
    note = get_object_or_404(Note, pk=note_id)
    note.increment_download_count()
    return redirect(note.file.url) # Or serve the file directly

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login after registration
    else:
        form = UserCreationForm()
    return render(request, 'notes\templates\notes\registration\register.html', {'form': form})  # Updated template path