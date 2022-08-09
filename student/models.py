from django.db import models
from courses.models import Courses
# Create your models here.

class StudentCourseApplication(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    address  = models.CharField(max_length=200)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    appplied_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.full_name} - {self.course.name}'
    
    class Meta:
        unique_together = ('email', 'course')
    