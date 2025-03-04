from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager

class Note(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='notes/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    tags = TaggableManager()
    download_count = models.IntegerField(default=0)
    status = models.CharField(max_length=20, default='pending')

    YEAR_CHOICES = [('1', 'First Year'), ('2', 'Second Year'), ('3', 'Third Year'), ('4', 'Fourth Year')]
    SEMESTER_CHOICES = [('1', 'Semester 1'), ('2', 'Semester 2')]

    year = models.CharField(max_length=1, choices=YEAR_CHOICES, default='1')
    semester = models.CharField(max_length=1, choices=SEMESTER_CHOICES, default='1')
    subject = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.title

    def increment_download_count(self):
        self.download_count += 1
        self.save()
