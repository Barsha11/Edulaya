from django.urls import path
from .views import *

app_name="students"

urlpatterns = [
    path('', student_index, name='student_index'),
]