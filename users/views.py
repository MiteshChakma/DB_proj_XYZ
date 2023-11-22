from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import User  
from django.http import HttpResponseRedirect
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

# Login View
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)

            if user.is_administrator():
                return redirect('admin_dashboard')
            elif user.is_customer():
                return redirect('customer_dashboard')
            elif user.is_customer_service():
                return redirect('customer_service_dashboard')
            elif user.is_db_administrator():
                return redirect('dba_dashboard')
            else:
                return redirect('default_page')
        else:
            # Handle invalid login here
            pass

    return render(request, 'login.html')

# Register View
from .forms import CustomUserCreationForm
from django.contrib.auth import login as auth_login

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Assign a role to the user if necessary
            user.role = User.CUSTOMER  # For example
            user.save()

            auth_login(request, user)

            # Redirect based on user role
            return redirect('appropriate_dashboard')
    else:
        form = CustomUserCreationForm()

    return render(request, 'register.html', {'form': form})



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

