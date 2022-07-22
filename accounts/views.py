from django.shortcuts import render, redirect
from accounts.models import Account
from .forms import NewUserForm, CustomAuthForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.http.response import JsonResponse
from rest_framework import status
import requests
from courses.models import *

def homepage(request):
    courses = Courses.objects.all()
    return render(request, template_name="index.html", context={'courses':courses})


def register(request):
    if request.method == "POST":
        context = {}
        full_name = request.POST['full_name']
        email = request.POST['email']
        role = request.POST['role']
        phone = request.POST['phone']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password != confirm_password:
            context['message'] = 'Password and Confirm Password Do Not Match'
            context['code'] = status.HTTP_400_BAD_REQUEST
            return JsonResponse(context, status=200)
        
        if Account.objects.filter(email=email).exists():
            context['message'] = 'Email Already Exists'
            context['code'] = status.HTTP_400_BAD_REQUEST
            return JsonResponse(context, status=200)
        
        else:
            user = Account.objects.create_user(
                full_name=full_name, email=email, password=password, role=role, phone=phone)
            messages.success(request, 'Thank you for registering with us')
            context={'message':'Thank you for registering with us.','code':status.HTTP_200_OK}
            return JsonResponse(context, status=201)

def login_request(request):
    if request.method == "POST":
        context={}
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(email=email, password=password)
        
        if user is None:
            context['message1'] = 'Invalid Login Details!'
            context['message2'] = 'Please Try Again With A Valid Email And Password'
            context['code'] = status.HTTP_401_UNAUTHORIZED
            return JsonResponse(context, status=200)
        
        elif user is not None:
            login(request, user)
            context['message'] = 'Successfully authenticated.'
            context['status'] = 'Success!'
            context['code'] = status.HTTP_200_OK
            context['role'] = user.role
            messages.success(request, 'You are now logged in.')
            url = request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlparse(url).query
                params = dict(x.split("=") for x in query.split('&'))
                if 'next' in params:
                    nextpage = params['next']
                    return redirect(nextpage)     

            except:
                return JsonResponse(context, status=200)        
        else:
            context['message'] = 'Invalid credentials'
            context['message2'] = 'Kindly Try Again With A Valid Email And Password'
            context['code'] = status.HTTP_401_UNAUTHORIZED
            return JsonResponse(context, status=400)
    return JsonResponse({'action':'Not allowed'}, status=400)

def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("authentication:homepage")