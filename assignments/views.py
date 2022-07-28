from django.http import JsonResponse
from django.shortcuts import render

from assignments.models import *

# Create your views here.
def AssignmentSubmissionView(request):
    if request.method == 'POST':
        title = request.POST.get('title', None)
        assignment_id = request.POST.get('assignment', None) 
        
        file = request.FILES.get('files[]', None)

        if title and assignment_id and file:
            assignment = Assignments.objects.get(id=assignment_id)
            assignment_submission = AssignmentSubmission(assignment=assignment, file=file)
            assignment_submission.submitted_by = request.user
            assignment_submission.save()
            return JsonResponse({'msg':'<span style="color: green;">Assignment successfully uploaded</span>'})
        else:
            return JsonResponse({'msg':'<span style="color: red;">Error</span>'})
        
def AssignmentCreationView(request):
    title = request.POST.get('assignment-title', None)
    description = request.POST.get('assignment-description', None) 
    marks = request.POST.get('assignment-marks', None) 
    deadline = request.POST.get('assignment-deadline', None) 
    course = request.POST.get('course', None) 
    file = request.FILES.get('files[]', None)

    if title and course:
        assignment = Assignments()
        assignment.title = title
        assignment.description = description
        assignment.full_marks = marks
        assignment.deadline = deadline
        assignment.course = Courses.objects.get(id=course)
        assignment.file = file
        assignment.save()
        return JsonResponse({'msg':'<span style="color: green;">Assignment successfully Created</span>'})
    else:
            return JsonResponse({'msg':'<span style="color: red;">Error</span>'})
        