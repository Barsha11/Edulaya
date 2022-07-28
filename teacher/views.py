from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from assignments.models import AssignmentSubmission, Assignments
from django.db.models import Value, CharField, Case, When, F, Subquery, OuterRef
from courses.models import CourseEnrollment
from library.models import Ebook
from chat.models import Thread

@login_required(login_url='/')
def teacher_index(request):
    user = request.user
    threads = Thread.objects.by_user(user=request.user).prefetch_related('chatmessage_thread').order_by('timestamp')
    context = {
        'Threads': threads,
        'user':user
    }
    return render(request, 'teachers.html', context)