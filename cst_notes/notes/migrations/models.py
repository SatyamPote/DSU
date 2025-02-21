from django.db import models

class Note(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='notes/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
