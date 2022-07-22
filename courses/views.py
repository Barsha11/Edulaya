from django.http import JsonResponse
from django.shortcuts import render
from .models import *
# Create your views here.
def courses(request):
    courses = Courses.objects.all()
    data = list(courses.values())
    return JsonResponse(data, safe=False)
    