from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from assignments.models import AssignmentSubmission, Assignments
from django.db.models import Value, CharField, Case, When, F, Subquery, OuterRef
from courses.models import CourseEnrollment, Courses
from library.models import Ebook
from chat.models import Thread

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