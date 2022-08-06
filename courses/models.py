from django.db import models

    
class Courses(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    description=models.TextField(blank=True)
    tutor = models.ForeignKey('accounts.Account', on_delete=models.CASCADE, related_name='tutor_courses', null=True, blank=True)
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
    
    
class CourseEnrollment(models.Model):
    student = models.ForeignKey('accounts.Account', on_delete=models.CASCADE, related_name='student_courses')
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    
    