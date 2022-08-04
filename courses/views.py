from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render
from .models import *
# Create your views here.
def courses(request):
    courses = Courses.objects.all()
    data = list(courses.values())
    return JsonResponse(data, safe=False)
    
def courses_list(request):
    courses = Courses.objects.all()
    return render(request, "admin2/courses.html", {"courses": courses})

class coursesUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Courses
    template_name = 'courses_edit.html'
    fields = '__all__'
    success_url = reverse_lazy('courses:courses_admin_list')
    success_message = "Updated Successfully"
    # permission_required = 'DashboardImg.change_dashboardimage'

class coursesDelete(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Courses
    template_name = 'modal/confirm_delete.html'
    success_url = reverse_lazy('courses:courses_admin_list')
