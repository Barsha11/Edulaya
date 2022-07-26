from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from assignments.models import AssignmentSubmission, Assignments
from django.db.models import Value, CharField, Case, When, F, Subquery, OuterRef
from courses.models import CourseEnrollment


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
    context = {
        'courses': courses,
        'assignments': assignments,
        'course_count': course_count,
        'assignment_count': assignment_count,
    }
    return render(request, 'student-dashboard.html', context)