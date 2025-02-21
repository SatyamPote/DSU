from django.db import models

class Note(models.Model):
    SUBJECT_CHOICES = [
        ('DSA', 'Data Structures & Algorithms'),
        ('OS', 'Operating Systems'),
        ('DBMS', 'Database Management Systems'),
        ('CN', 'Computer Networks'),
        ('AI', 'Artificial Intelligence'),
        # Add more subjects as needed
    ]

    title = models.CharField(max_length=255)
    subject = models.CharField(max_length=10, choices=SUBJECT_CHOICES)
    file = models.FileField(upload_to='notes/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.get_subject_display()}"
