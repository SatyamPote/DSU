from django.urls import path
from .views import home, notes

urlpatterns = [
    path('', home, name='home'),
    path('notes/', notes, name='notes'),
]
