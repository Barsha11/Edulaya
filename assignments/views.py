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