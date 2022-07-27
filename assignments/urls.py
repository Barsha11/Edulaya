from django.urls import path
from .views import *

app_name="assignments"

urlpatterns = [
    path('assignment-submit', AssignmentSubmissionView, name='assignment_submit'),
]