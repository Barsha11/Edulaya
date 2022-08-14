from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, render
from accounts.models import Account
from courses.forms import CoursesForm
from .models import *
# Create your views here.
def courses(request):
    courses = Courses.objects.all()
    data = list(courses.values())
    return JsonResponse(data, safe=False)
    
def courses_list(request):
    courses = Courses.objects.all()
    return render(request, "admin2/courses.html", {"courses": courses, 'title': 'courses'})

class coursesAdd(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model=Courses
    fields='__all__'
    template_name = 'courses_add.html'
    success_url = reverse_lazy('courses:courses_admin_list')
    success_message = "New Course added successfully"

    def get_context_data(self, **kwargs):
        data = super(coursesAdd, self).get_context_data(**kwargs)
        data['form'].fields['tutor'].queryset = Account.objects.filter(role="Teacher")
        if self.request.POST:
            data['items'] = CoursesForm(self.request.POST)
        else:
            data['items'] = CoursesForm()
            data['title'] = 'courses'
            
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        form=context['form']
        if form.is_valid():
            # form.instance.created_by=self.request.user
            # form.instance=form.save(commit=False)
            # try:
            #     itemx = get_object_or_404(Courses, status=True)
            #     itemx.status=False
            #     itemx.save()
            # except:
            form.save()
        return super(coursesAdd, self).form_valid(form)


class coursesUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Courses
    template_name = 'courses_edit.html'
    fields = '__all__'
    success_url = reverse_lazy('courses:courses_admin_list')
    success_message = "Updated Successfully"
    
    def get_context_data(self, **kwargs):
        data = super(coursesUpdate, self).get_context_data(**kwargs)
        data['form'].fields['tutor'].queryset = Account.objects.filter(role="Teacher")
        if self.request.POST:
            data['items'] = CoursesForm(self.request.POST)
        else:
            data['items'] = CoursesForm()
            data['title'] = 'courses'
            data['name'] = 'Update Course'
        return data

class coursesDelete(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Courses
    template_name = 'modal/confirm_delete.html'
    success_url = reverse_lazy('courses:courses_admin_list')
    
    def get_context_data(self, **kwargs):
        data = super(coursesDelete, self).get_context_data(**kwargs)
        data['title'] = 'courses'
        return data

# class coursesTeacherAssign(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
#     model = Courses
#     template_name = 'courses_edit.html'
#     fields = ['name','tutor']
#     success_url = reverse_lazy('courses:courses_admin_list')
#     success_message = "Updated Successfully"
    
#     def get_context_data(self, **kwargs):
#         data = super(coursesUpdate, self).get_context_data(**kwargs)
#         data['form'].fields['tutor'].queryset = Account.objects.filter(role="Teacher")
#         if self.request.POST:
#             data['items'] = CoursesForm(self.request.POST)
#         else:
#             data['items'] = CoursesForm()
#             data['title'] = 'courses'
#         return data
    
@login_required(login_url='/')
def coursesTeacherAssign(request):
    courses = Courses.objects.all()
    return render(request, "course_teacher_assign.html", {"courses": courses, 'title': 'Assign Courses'})

class TeacherAssigncoursesUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Courses
    template_name = 'courses_edit.html'
    fields = ['name', 'tutor']
    success_url = reverse_lazy('courses:assign_course')
    success_message = "Updated Successfully"
    
    def get_context_data(self, **kwargs):
        data = super(TeacherAssigncoursesUpdate, self).get_context_data(**kwargs)
        data['form'].fields['tutor'].queryset = Account.objects.filter(role="Teacher")

        if self.request.POST:
            data['items'] = CoursesForm(self.request.POST)
        else:
            data['items'] = CoursesForm()
            data['title'] = 'Assign Courses'
            data['name'] = 'Assign Course'
            
        return data
    
    def get_form(self, form_class=None):
        form = super(TeacherAssigncoursesUpdate, self).get_form(form_class)
        form.fields["name"].disabled = True
        return form