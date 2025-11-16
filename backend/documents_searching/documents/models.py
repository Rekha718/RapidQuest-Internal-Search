from django.db import models

class Document(models.Model):
    
    file_id = models.CharField(max_length=255, blank=True, null=True)  # Appwrite file ID
    filename = models.CharField(max_length=255)
    normalized_filename = models.CharField(max_length=300, blank=True)
    content = models.TextField(blank=True)   # extracted text
    keywords = models.TextField(blank=True)  # comma separated keywords
    category = models.CharField(max_length=100, blank=True)  # auto category
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.filename
