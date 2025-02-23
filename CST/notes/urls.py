from django.urls import path
from . import views
from .views import redirect_to_admin

urlpatterns = [
    path('', views.home, name='home'),
    path('notes/', views.notes_list, name='notes'),
    path('upload/', views.note_upload, name='note_upload'),
    path('download/<int:note_id>/', views.download_note, name='download_note'),
    path('register/', views.register, name='register'),  # Add this line
    path('admin-login/', redirect_to_admin, name='admin_login_redirect'),
]