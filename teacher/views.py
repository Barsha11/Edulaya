from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from accounts.models import Account
from assignments.models import Assignments
from courses.models import Courses
from library.models import Ebook
from chat.models import Thread
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, render

from teacher.forms import CreateUserForm, UserSetPasswordForm, UserUpdateForm

@login_required(login_url='/')
def teacher_index(request):
    courses = Courses.objects.filter(tutor=request.user)
    user = request.user
    threads = Thread.objects.by_user(user=request.user).prefetch_related('chatmessage_thread').order_by('timestamp')
    assignments = Assignments.objects.filter(course__in=courses)
    ebook_courses = Ebook.objects.all()
    context = {
        'Threads': threads,
        'user':user,
        'courses': courses,
        'assignments': assignments,
        'ebook_courses':ebook_courses,
        
    }
    return render(request, 'teachers.html', context)

def teachers_list(request):
    teachers = Account.objects.filter(role='Teacher')
    context = {
        'teachers': teachers,
    }
    return render(request, 'teachers_list.html', context)


def teacherAdd(request):
    user_form = CreateUserForm()
    if request.method == "POST":
        user_form = CreateUserForm(request.POST)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            if user.email:
                user.email = user.email.lower()
            user.is_active = True
            user.role = 'Teacher'
            user.save()
            return redirect("teacher:teachers_admin_list")
    context = {"form": user_form, "title": "teacher"}
    return render(request, "teachers_add.html", context)


def teacher_update(request, id):
    user = Account.objects.get(id=id)
    form = UserUpdateForm(instance=user)
    if request.method == "POST":
        form = UserUpdateForm(
            request.POST,
            request.FILES,
            instance=user,
        )
        if form.is_valid():
            user = form.save(commit=False)
            if user.email:
                user.email = user.email.lower()
            user.save()
            return redirect("teacher:teachers_admin_list")

    context = {"form": form, "title": "teacher"}
    return render(request, "teachers_edit.html", context)

def teacher_change_password(request, id):
    if request.user.is_superadmin:
        user = get_object_or_404(Account, id=id)
        form = UserSetPasswordForm(user)
        if request.method == "POST":
            form = UserSetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                return redirect("teacher:teachers_admin_list")
        context = {
            "form": form,
        }
        return render(request, "password_change.html", context=context)
    return redirect("teacher:teachers_admin_list")

class TeacherDelete(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Account
    template_name = 'modal/confirm_delete.html'
    success_url = reverse_lazy('teacher:teachers_admin_list')
    
    def get_context_data(self, **kwargs):
        data = super(TeacherDelete, self).get_context_data(**kwargs)
        data['title'] = 'teacher'
        return data
