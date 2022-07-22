from django.urls import path
from .views import *

app_name="courses"

urlpatterns = [
    path('course-list', courses, name='courses_list'),
]