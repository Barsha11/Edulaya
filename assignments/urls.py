from django.urls import path
from .views import *

app_name="assignments"

urlpatterns = [
    path('assignment-submit', AssignmentSubmissionView, name='assignment_submit'),
    path('assignment-review', AssignmentReviewView, name='assignment_review'),
    path('assignment-create', AssignmentCreationView.as_view(), name='assignment_create'),
    path('assignment-edit/<int:pk>',AssignmentUpdateView.as_view(),name='assignment_edit'),
    
]