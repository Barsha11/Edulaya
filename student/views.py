from urllib.parse import non_hierarchical
from django.contrib.auth.decorators import login_required
from assignments.models import AssignmentSubmission, Assignments
from django.db.models import Subquery, OuterRef
from django.db import transaction
from django.http.response import JsonResponse
import string
import random
from datetime import datetime
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
from .models import StudentCourseApplication
from teacher.forms import CreateUserForm, UserSetPasswordForm, UserUpdateForm
from chat.models import Thread
from django.core.mail import send_mail
from django.contrib.auth.decorators import user_passes_test

def user_check(user):
    return user.role == 'Student'


@login_required(login_url='/')
@user_passes_test(user_check)
def student_index(request):
    courses = CourseEnrollment.objects.filter(student=request.user)
    course_count = courses.count()
    student_courses = courses.values_list('course', flat=True)
    submitted_assignments = AssignmentSubmission.objects.filter(submitted_by=request.user).values_list('assignment', flat=True)
    
    scheduled_assignments = Assignments.objects.filter(course__in=student_courses, is_scheduled=True, scheduled_time__lte=datetime.now())
    assignments = Assignments.objects.filter(course__in=student_courses, is_scheduled=False)
    assignments = scheduled_assignments | assignments
    assignments = assignments.annotate(
        assignment_status = Subquery(
            AssignmentSubmission.objects.filter(assignment=OuterRef("id")).values_list('status', flat=True)
        ))
    assignments_dropdown = Assignments.objects.filter(course__in=student_courses).exclude(id__in=submitted_assignments)
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
        'assignments_dropdown': assignments_dropdown,
        'asignment_checked_count': asignment_checked_count,
        'submitted_assignments': submitted_assignments,
        'ebook_courses':ebook_courses,
        'Threads': threads,
        'user':user
    }
    return render(request, 'student-dashboard.html', context)

@login_required(login_url='/')
def students_list(request):
    students = Account.objects.filter(role='Student')
    context = {
        'students': students,
    }
    return render(request, 'students_list.html', context)

@login_required(login_url='/')
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

@login_required(login_url='/')
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

@login_required(login_url='/')
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

@login_required(login_url='/')
def StudentCourseRequestCreationView(request):
    full_name = request.POST.get('full_name', None)
    email = request.POST.get('email', None) 
    phone = request.POST.get('phone', None) 
    address = request.POST.get('address', None) 
    course = request.POST.get('course', None)
    
    if  StudentCourseApplication.objects.filter(email = email, course_id=course):
        return JsonResponse({'msg':'<span style="color: red;">You have already applied for this course</span>'})
    
    if full_name and phone and course:
        application = StudentCourseApplication()
        application.full_name = full_name
        application.email = email
        application.phone_number = phone
        application.address = address
        application.course = Courses.objects.get(id=course)
        application.save()
        return JsonResponse({'msg':'<span style="color: green;">You have successfully Applied for the Course</span>'})
    else:
            return JsonResponse({'msg':'<span style="color: red;">Error</span>'})
        
@login_required(login_url='/')  
def StudentCourseRequestView(request):
    applications = StudentCourseApplication.objects.all().order_by('appplied_date')
    context = {
        'applications': applications,
    }
    return render(request, 'student-course-request.html', context)


class StudentCourseRequestDelete(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = StudentCourseApplication
    template_name = 'modal/confirm_delete.html'
    success_url = reverse_lazy('students:student_course_request')
    
    def get_context_data(self, **kwargs):
        data = super(StudentCourseRequestDelete, self).get_context_data(**kwargs)
        data['title'] = 'enroll-request'
        return data
    

def generate_code(request):
    letters = string.ascii_lowercase
    result_str = "".join(random.choice(letters) for i in range(10))
    return result_str

@login_required(login_url='/')
def StudentCourseRequestApprove(request, id):
    student_data = StudentCourseApplication.objects.get(id=id)
    try:
        with transaction.atomic():
            student_user  = Account.objects.get(email=student_data.email)
            CourseEnrollment.objects.create(course=student_data.course, student=student_user)
            try:
                a=Thread.objects.create(first_person=student_user, second_person=student_data.course.tutor)
            except:
                a=None
            student_data.delete()
    except:
        with transaction.atomic():
            student_user = Account(
                full_name = student_data.full_name,
                email = student_data.email,
                phone_number = student_data.phone_number,
                role = 'Student'
            )
            password = generate_code(request)
            student_user.set_password(password)
            student_user.is_active = True
            student_user.save()
            
            CourseEnrollment.objects.create(course=student_data.course, student=student_user)
            try:
                a=Thread.objects.create(first_person=student_user, second_person=student_data.course.tutor)
            except:
                a=None
            subject = 'Enrollment Confirmation'  
            from_email = 'no_reply@learning.com'
            recipient_list=[student_data.email]
            message = f'Hello {student_data.full_name},\n\nYou have been enrolled in {student_data.course.name} course.\n\nYour login credentials are:\n\nUsername: {student_data.email}\nPassword: {password}\n\nPlease login and change your password.\n\nThanks,\nLearning Team'
            send_mail(subject, from_email=from_email,recipient_list=recipient_list,message=message)
            student_data.delete() 
            
                   
    applications = StudentCourseApplication.objects.all().order_by('appplied_date')
    context = {
        'applications': applications,
    }
    return redirect('students:student_course_request')
    # return render(request, 'student-course-request.html', context)