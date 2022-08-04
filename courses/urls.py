from django.urls import path
from .views import *

app_name="courses"

urlpatterns = [
    path('course-list', courses, name='courses_list'),
    path('all-courses', courses_list, name='courses_admin_list'),
    path('edit/<int:pk>',coursesUpdate.as_view(),name='courses_edit'),
   path('delete/<int:pk>',coursesDelete.as_view(),name='courses_delete'),
]