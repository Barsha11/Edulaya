from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Layout, Row,Column
from django.forms import ModelForm
from django import forms
from .models import *

class CoursesForm(ModelForm):
    class Meta:
        model=Courses
        fields='__all__'