from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse
from django.http import JsonResponse, HttpResponse
import re
import wikipedia
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Note
from .forms import NoteForm
import pyrebase


config={
    "apiKey": "AIzaSyC5h8gEZbusQ8PN89Da-5HJpSRDNtEmgL4",
    "authDomain": "cstnotes-f0e59.firebaseapp.com",
    "databaseURL": "https://cstnotes-f0e59-default-rtdb.firebaseio.com",
    "projectId": "cstnotes-f0e59",
    "storageBucket": "cstnotes-f0e59.firebasestorage.app",
    "messagingSenderId": "17433439165",
    "appId": "1:17433439165:web:70213cd44c15c4ea2b40d4",
    "measurementId": "G-5FGDKSLYGY"
}

firebase = pyrebase.initialize_app(config)
authe=firebase.auth()
database=firebase.database()

def health_check(request):
    return HttpResponse("OK")

def add_note_to_firebase(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        data = {
            "title": title,
            "content": content,
            "user_id": request.session.get('uid')
        }
        try:
            database.child("notes").push(data)
            return JsonResponse({'message': 'Note added successfully'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return render(request, 'notes/note_upload.html')

def home(request):
    years = Note.YEAR_CHOICES
    semesters = Note.SEMESTER_CHOICES
    card_data = []

    for year_choice in years:
        for semester_choice in semesters:
            notes = Note.objects.filter(year=year_choice[0], semester=semester_choice[0])[:3]  # Get first 3 notes
            card_data.append({
                'year': year_choice,
                'semester': semester_choice,
                'notes': notes,
            })

    context = {'card_data': card_data}
    return render(request, 'home.html', context)

def notes_list(request):
    query = request.GET.get('q')
    year = request.GET.get('year')
    semester = request.GET.get('semester')
    subject = request.GET.get('subject')

    notes = Note.objects.all()

    if query:
        notes = notes.filter(
            Q(title__icontains=query) | Q(category__icontains=query) | Q(tags__name__icontains=query)
        ).distinct()

    if year:
        notes = notes.filter(year=year)
    if semester:
        notes = notes.filter(semester=semester)
    if subject:
        notes = notes.filter(subject=subject)

    return render(request, 'notes/notes.html', {'notes': notes, 'query': query, 'year': year, 'semester': semester})

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
    return redirect(note.file.url)

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Auto login after registration
            return redirect('home')  # Redirect to homepage after registration
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def notes_by_criteria(request):
    year = request.GET.get('year')
    semester = request.GET.get('semester')

    notes = Note.objects.all()

    if year:
        notes = notes.filter(year=year)
    if semester:
        notes = notes.filter(semester=semester)

    return render(request, 'notes/notes_by_criteria.html', {'notes': notes, 'year': year, 'semester': semester})

def staff_login(request):
    return redirect('admin:login')  # Redirect to Django admin login page

def test_view(request):
    return HttpResponse("Hello, world!")

def get_subjects(request):
    year = request.GET.get('year')
    semester = request.GET.get('semester')

    subjects = {
        '1': {
            '1': ['Mathematics I', 'Physics I', 'Programming I'],
            '2': ['Mathematics II', 'Physics II', 'Programming II'],
        },
        '2': {
            '1': ['Data Structures', 'Algorithms', 'Operating Systems'],
            '2': ['Databases', 'Software Engineering', 'Computer Networks'],
        },
        '3': {
            '1': ['Subject 1', 'Subject 2', 'Subject 3'],
            '2': ['Subject 4', 'Subject 5', 'Subject 6'],
        },
        '4': {
            '1': ['Subject 7', 'Subject 8', 'Subject 9'],
            '2': ['Subject 10', 'Subject 11', 'Subject 12'],
        }
    }

    if year and semester:
        subject_list = subjects.get(year, {}).get(semester, [])
    else:
        subject_list = []

    return JsonResponse({'subjects': subject_list})

def custom_logout(request):
    logout(request)
    return redirect('home')

def chatbot(request):
    if request.method == 'POST':
        question = request.POST.get('question')

        # Load all notes related to computer science
        notes = Note.objects.filter(subject='cs')
        context = ""

        for note in notes:
            try:
                note.file.open()  # Open file before reading
                file_content = note.file.read().decode('utf-8')
                note.file.close()
                context += file_content + "\n"
            except Exception as e:
                context += f"Error reading file {note.title}: {e}"

        answer = search_keyword(question, context)
        if "I'm sorry" in answer:
            try:
                answer = wikipedia.summary(f"{question} computer science", sentences=3)
            except wikipedia.exceptions.PageError:
                answer = "I'm sorry, I couldn't find information about that topic on Wikipedia either."
            except wikipedia.exceptions.DisambiguationError as e:
                answer = f"I found multiple pages for that query. Can you be more specific? {e.options}"

        return render(request, 'chatbot.html', {'question': question, 'answer': answer})
    
    return render(request, 'chatbot.html')

def search_keyword(keyword, context, num_sentences=3):
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', context)
    relevant_sentences = [s for s in sentences if keyword.lower() in s.lower()]

    if relevant_sentences:
        first_index = sentences.index(relevant_sentences[0])
        start_index = max(0, first_index - num_sentences // 2)
        end_index = min(len(sentences), first_index + num_sentences // 2 + 1)
        answer = " ".join(sentences[start_index:end_index])

        formatted_answer = "<ul>"
        for sentence in answer.split(". "):
            formatted_answer += f"<li>{sentence}.</li>"
        formatted_answer += "</ul>"
        return formatted_answer
    else:
        return "I'm sorry, I couldn't find information about that topic in the notes."
