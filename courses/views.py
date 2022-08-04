from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, render
from courses.forms import CoursesForm
from .models import *
# Create your views here.
def courses(request):
    courses = Courses.objects.all()
    data = list(courses.values())
    return JsonResponse(data, safe=False)
    
def courses_list(request):
    courses = Courses.objects.all()
    return render(request, "admin2/courses.html", {"courses": courses})

class coursesAdd(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model=Courses
    fields='__all__'
    template_name = 'courses_add.html'
    success_url = reverse_lazy('courses:courses_admin_list')
    success_message = "New Course added successfully"

    def get_context_data(self, **kwargs):
        data = super(coursesAdd, self).get_context_data(**kwargs)
        if self.request.POST:
            data['items'] = CoursesForm(self.request.POST)
        else:
            data['items'] = CoursesForm()
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
    # permission_required = 'DashboardImg.change_dashboardimage'

class coursesDelete(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Courses
    template_name = 'modal/confirm_delete.html'
    success_url = reverse_lazy('courses:courses_admin_list')
