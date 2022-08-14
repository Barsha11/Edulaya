from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from assignments.forms import AssignmentsForm
from assignments.models import *

# Create your views here.
@login_required(login_url='/')
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
        
# def AssignmentCreationView(request):
#     title = request.POST.get('assignment-title', None)
#     description = request.POST.get('assignment-description', None) 
#     marks = request.POST.get('assignment-marks', None) 
#     deadline = request.POST.get('assignment-deadline', None) 
#     course = request.POST.get('course', None) 
#     file = request.FILES.get('files[]', None)

#     if title and course:
#         assignment = Assignments()
#         assignment.title = title
#         assignment.description = description
#         assignment.full_marks = marks
#         assignment.deadline = deadline
#         assignment.course = Courses.objects.get(id=course)
#         assignment.file = file
#         assignment.save()
#         return JsonResponse({'msg':'<span style="color: green;">Assignment successfully Created</span>'})
#     else:
#             return JsonResponse({'msg':'<span style="color: red;">Error</span>'})
        
# 
class AssignmentCreationView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model=Assignments
    fields='__all__'
    template_name = 'createassignment.html'
    success_url = reverse_lazy('teacher:teacher_index')
    success_message = "New Assignment added successfully"

    def get_context_data(self, **kwargs):
        data = super(AssignmentCreationView, self).get_context_data(**kwargs)
        data['form'].fields['course'].queryset = Courses.objects.filter(tutor=self.request.user)
        
        if self.request.POST:
            data['items'] = AssignmentsForm(self.request.POST, self.request.FILES)
        else:
            data['items'] = AssignmentsForm()
            data['title'] = 'Add Assignment'
            
        return data

    def form_valid(self, form):
        form=AssignmentsForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            form.save()
        else:
            return self.render_to_response(self.get_context_data(form=form))
        return super(AssignmentCreationView, self).form_valid(form)
    
class AssignmentUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Assignments
    template_name = 'editassignment.html'
    fields = '__all__'
    success_url = reverse_lazy('teacher:teacher_index')
    success_message = "Updated Successfully"
    
    def get_context_data(self, **kwargs):
        data = super(AssignmentUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['items'] = AssignmentsForm(self.request.POST)
        else:
            data['items'] = AssignmentsForm()
        return data