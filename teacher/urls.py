from django.urls import path
from .views import *

app_name="teacher"

urlpatterns = [
    path('', teacher_index, name='teacher_index'),
]