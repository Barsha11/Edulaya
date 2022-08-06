from django.contrib.auth.decorators import login_required
from assignments.models import AssignmentSubmission, Assignments
from django.db.models import Subquery, OuterRef
from chat.models import Thread
from courses.models import CourseEnrollment,Courses
from library.models import Ebook
from django.shortcuts import render, redirect
from accounts.models import Account
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, render

from teacher.forms import CreateUserForm, UserSetPasswordForm, UserUpdateForm


@login_required(login_url='/')
def student_index(request):
    courses = CourseEnrollment.objects.filter(student=request.user)
    course_count = courses.count()
    student_courses = courses.values_list('course', flat=True)
    assignments = Assignments.objects.filter(course__in=student_courses).annotate(
        # assignment_status = Value('s', output_field=CharField()),
        assignment_status = Subquery(
            # Case(
            #     When(
                    AssignmentSubmission.objects.filter(assignment=OuterRef("id")).values_list('status', flat=True)
                    # [0] == 'None', 
                    # then='Submission Pending')
            # )
        )
    )
    assignment_count = assignments.count()
    asignment_checked_count = AssignmentSubmission.objects.filter(submitted_by=request.user, status='Checked').count()
    ebook_courses = Ebook.objects.all()
    user = request.user
    threads = Thread.objects.by_user(user=request.user).prefetch_related('chatmessage_thread').order_by('timestamp')
    context = {
        'courses': courses,
        'assignments': assignments,
        'course_count': course_count,
        'assignment_count': assignment_count,
        'asignment_checked_count': asignment_checked_count,
        'ebook_courses':ebook_courses,
        'Threads': threads,
        'user':user
    }
    return render(request, 'student-dashboard.html', context)


def students_list(request):
    students = Account.objects.filter(role='Student')
    context = {
        'students': students,
    }
    return render(request, 'students_list.html', context)


def studentAdd(request):
    user_form = CreateUserForm()
    if request.method == "POST":
        user_form = CreateUserForm(request.POST)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            if user.email:
                user.email = user.email.lower()
            user.is_active = True
            user.role = 'Student'
            user.save()
            return redirect("students:students_admin_list")
    context = {"form": user_form, "title": "Student"}
    return render(request, "students_add.html", context)


def student_update(request, id):
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
            return redirect("students:students_admin_list")

    context = {"form": form, "title": "Student"}
    return render(request, "students_edit.html", context)

def student_change_password(request, id):
    if request.user.is_superadmin:
        user = get_object_or_404(Account, id=id)
        form = UserSetPasswordForm(user)
        if request.method == "POST":
            form = UserSetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                return redirect("students:students_admin_list")
        context = {
            "form": form,
        }
        return render(request, "password_change.html", context=context)
    return redirect("students:students_admin_list")

class StudentDelete(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Account
    template_name = 'modal/confirm_delete.html'
    success_url = reverse_lazy('students:students_admin_list')
    
    def get_context_data(self, **kwargs):
        data = super(StudentDelete, self).get_context_data(**kwargs)
        data['title'] = 'Student'
        return data
