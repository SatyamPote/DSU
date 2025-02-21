from django.contrib import admin
from .models import Note

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'uploaded_by', 'upload_date')
    search_fields = ('title', 'uploaded_by')
    list_filter = ('category', 'upload_date')
