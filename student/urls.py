from django.urls import path
from .views import *

app_name="students"

urlpatterns = [
    path('', student_index, name='student_index'),
    path('all-students', students_list, name='students_admin_list'),
    path('add/',studentAdd,name='student_add'),
    path('edit/<id>/',student_update,name='student_edit'),
    path('edit/<id>/password/',student_change_password,name="change_password"),
    path('delete/<int:pk>',StudentDelete.as_view(),name='student_delete'),
]