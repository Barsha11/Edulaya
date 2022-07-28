from django.db import models
from courses.models import Courses
# Create your models here.
class Assignments(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    file = models.FileField(upload_to='assignment-question/', null=True, blank=True)
    full_marks = models.IntegerField()
    course = models.ForeignKey(Courses, on_delete=models.CASCADE, related_name='assignments_course')
    created_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField()
    
    def __str__(self):
        return self.title
    
class AssignmentSubmission(models.Model):
    status = (
        ('Submission Pending', 'Submission Pending'),
        ('Review Pending', 'Review Pending'),
        ('Checked', 'Checked'),
        ('Rejected', 'Rejected'),
    )
    assignment = models.ForeignKey(Assignments, on_delete=models.CASCADE, related_name='assignment_submission')
    file = models.FileField(upload_to='assignment-submissions/', null=True, blank=True)
    submitted_by = models.ForeignKey('accounts.Account', on_delete=models.CASCADE, related_name='assignment_submission_user')
    submitted_at = models.DateTimeField(auto_now_add=True)
    marks = models.IntegerField(null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=status, default='Review Pending')
    
    def __str__(self):
        return self.assignment.title
    
    class Meta:
        unique_together = ('assignment', 'submitted_by')