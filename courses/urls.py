from django.urls import path
from .views import *

app_name="courses"

urlpatterns = [
    path('course-list', courses, name='courses_list'),
    path('all-courses', courses_list, name='courses_admin_list'),
    path('add/',coursesAdd.as_view(),name='courses_add'),
    path('edit/<int:pk>',coursesUpdate.as_view(),name='courses_edit'),
    path('delete/<int:pk>',coursesDelete.as_view(),name='courses_delete'),
    path('assign-course',coursesTeacherAssign, name='assign_course'),   
    path('assigned-course-edit/<int:pk>',TeacherAssigncoursesUpdate.as_view(),name='assigned_courses_edit'),
    
]