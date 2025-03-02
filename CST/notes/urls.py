from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('notes/', views.notes_list, name='notes'),
    path('upload/', views.note_upload, name='note_upload'),
    path('download/<int:note_id>/', views.download_note, name='download_note'),
    path('register/', views.register, name='register'),
    path('staff_login/', views.staff_login, name='staff_login'),
    path('get_subjects/', views.get_subjects, name='get_subjects'),
    path('logout/', views.custom_logout, name='custom_logout'),
    path('chatbot/', views.chatbot, name='chatbot'),
    path('download/<int:note_id>/', views.download_note, name='download_note'),

]
