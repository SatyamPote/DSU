from django.shortcuts import render, redirect, get_object_or_404
from .models import Note
from .forms import NoteForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .forms import StaffLoginForm  # Import StaffLoginForm
from django.http import JsonResponse
from django.contrib.auth import logout

def home(request):
    years = Note.YEAR_CHOICES
    semesters = Note.SEMESTER_CHOICES
    card_data = []

    for year_choice in years:
        for semester_choice in semesters:
            notes = Note.objects.filter(year=year_choice[0], semester=semester_choice[0])[:3]  # Get the first 3 notes
            card_data.append({
                'year': year_choice,
                'semester': semester_choice,
                'notes': notes,
            })

    context = {'card_data': card_data}
    return render(request, 'home.html', context)

#@login_required  # Remove this line if you want everyone to see the notes
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
    return redirect(note.file.url) # Or serve the file directly

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('staff_login')  # Redirect to staff login after registration
        else:
            return render(request, 'registration/register.html', {'form': form})
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})  # Updated template path

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
    if request.method == 'POST':
        form = StaffLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_staff:  # Check if the user is a staff member
                login(request, user)
                return redirect('notes')  # Redirect staff to notes list
            else:
                form.add_error(None, "Invalid staff credentials.")
        else:
            return render(request, 'registration/staff_login.html', {'form': form})
    else:
        form = StaffLoginForm()
    return render(request, 'registration/staff_login.html', {'form': form})

def get_subjects(request):
    year = request.GET.get('year')
    semester = request.GET.get('semester')

    # Define your subjects based on year and semester
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
        # Add more years and semesters as needed
    }

    if year and semester:
        subject_list = subjects.get(year, {}).get(semester, [])
    else:
        subject_list = []

    return JsonResponse({'subjects': subject_list})

def custom_logout(request):
    logout(request)
    return redirect('home')  # Redirect to the homepage after logout