from django.urls import path
from .views import *

app_name="teacher"

urlpatterns = [
    path('', teacher_index, name='teacher_index'),
    path('all-teachers', teachers_list, name='teachers_admin_list'),
    path('add/',teacherAdd,name='teacher_add'),
    path('edit/<id>/',teacher_update,name='teacher_edit'),
    path('edit/<id>/password/',teacher_change_password,name="change_password"),
    path('delete/<int:pk>',TeacherDelete.as_view(),name='teacher_delete'),
    path('assignment-check/<id>',assignment_submitted_list,name="assignment_check"),
]