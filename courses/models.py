from time import time
from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    
    def __str__(self):
        return self.name
    
class Courses(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    description=models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='courses-images', blank=True)
    time_to_complete=models.FloatField(default=0)
    
    def __str__(self):
        return self.name
    
class Course_documents(models.Model):
    course=models.ForeignKey(Courses, on_delete=models.CASCADE)
    file  = models.FileField(upload_to='course-documents/', null=True, blank=True)
    url = models.URLField(max_length=200, null=True, blank=True)
    
    def __str__(self):
        return f'{self.course.name} - {self.file.name}'
    