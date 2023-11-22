"""
URL configuration for DB_proj_XYZ project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from users import views  

# Import your views here

urlpatterns = [
    path('admin/', admin.site.urls),

    # Paths for user dashboards
    path('dashboard/customer/', views.customer_dashboard, name='customer_dashboard'),
    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/customer-service/', views.customer_service_dashboard, name='customer_service_dashboard'),
    path('dashboard/dba/', views.dba_dashboard, name='dba_dashboard'),

    # Paths for authentication
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    #path('', views.login_view, name='login'),

    # Add other paths as needed

    path('country_redirect/', views.redirect_to_country, name='redirect_to_country'),

    
    path('finland_dashboard/', views.finland_dashboard, name='finland_dashboard'),
    path('sweden_dashboard/', views.sweden_dashboard, name='sweden_dashboard'),
    #error page
    path('error/', views.error_page, name='error_page'),

    #home page
    path('', views.home, name='home'),
]

