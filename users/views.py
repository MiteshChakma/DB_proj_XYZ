from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import User  
from django.http import HttpResponseRedirect
from django.http import HttpResponse
import json
from django.forms.models import model_to_dict
# Import your User model

# Helper function to check roles
def is_customer(user):
    return user.is_customer()

def is_administrator(user):
    return user.is_administrator()

def is_customer_service(user):
    return user.is_customer_service()

def is_dba(user):
    return user.is_db_administrator()

# Dashboard Views
@login_required
@user_passes_test(is_customer)
def customer_dashboard(request):
    return render(request, 'customer_dashboard.html')

@login_required
@user_passes_test(is_administrator)
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')

@login_required
@user_passes_test(is_customer_service)
def customer_service_dashboard(request):
    return render(request, 'customer_service_dashboard.html')

@login_required
@user_passes_test(is_dba)
def dba_dashboard(request):
    return render(request, 'dba_dashboard.html')

def customAuth(username,password):
    try:
        user = User.objects.using('finland').get(username = username)
        if(user.check_password(password)):
            return user
        return 'password is incorrect'
    except User.DoesNotExist:
        try:
            user = User.objects.using('sweden').get(username = username)
            if(user.check_password(password)):
                return user
            return 'password is incorrect'
        except User.DoesNotExist:
            return None

# Login View
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        res= customAuth(username,password)
        if res == 'password is incorrect':
            return HttpResponse(json.dumps({'stu':0,'message': 'Password is incorrect'}))
        if res == None:
            return HttpResponse(json.dumps({'stu':0,'message': 'User is not existed'}))
        else:
            dictObj = model_to_dict(res)
            del dictObj['date_joined']
            del dictObj['last_login']
            user = json.dumps(dictObj)
            return HttpResponse(json.dumps({'stu':1,'message': user}))
    return HttpResponse(json.dumps({'stu':0,'message': 'Server error'}))

# Register View
from .forms import CustomUserCreationForm
from django.contrib.auth import login as auth_login

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user,status = form.save()
            if(status==''):
                return HttpResponse(json.dumps({'stu':1,'message': user}))
            return HttpResponse(json.dumps({'stu':0,'message': status}))
        else:
            return HttpResponse(json.dumps({'stu':0,'message': 'A user with that username already exists'}))
    return HttpResponse(json.dumps({'stu':0,'message': 'Server error'}))



def redirect_to_country(request):
    if request.method == 'POST':
        country = request.POST.get('country')

        if country == 'Finland':
            # Logic to connect to Finland's DB or redirect to Finland's dashboard
            return HttpResponseRedirect('/finland_dashboard/')
        elif country == 'Sweden':
            # Logic to connect to Sweden's DB or redirect to Sweden's dashboard
            return HttpResponseRedirect('/sweden_dashboard/')
    else:
        # Redirect back to the choice page or to an error page
        return HttpResponseRedirect('/error/')

def finland_dashboard(request):
    return render(request, 'finland_dashboard.html')

def sweden_dashboard(request):
    return render(request, 'sweden_dashboard.html')

def error_page(request):
    return render(request, 'error.html')

def home(request):
    return render(request, 'home.html')

