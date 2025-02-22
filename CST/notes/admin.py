from django.contrib import admin
from .models import Note

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploaded_at', 'uploaded_by', 'category', 'status', 'download_count')
    search_fields = ('title', 'uploaded_by__username', 'category', 'tags__name')
    list_filter = ('category', 'uploaded_at', 'status')
    # Removed filter_horizontal = ('tags',)