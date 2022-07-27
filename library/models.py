from django.db import models

# Create your models here.
class Ebook(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='ebooks/', blank=True)
    url=models.URLField(blank=True)
    
    def __str__(self):
        return self.title