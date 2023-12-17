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


# here are the URL paths

urlpatterns = [

    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('product_list/', views.getProductsList, name='product_list'),
    path('product/', views.getProduct, name='product'),
    path('warehouse_list/', views.getWarehousesList, name='warehouse_list'),
    path('warehouse/', views.getWarehouse, name='warehouse'),
    path('product-warehouse/', views.getProductWarehouses, name='product-warehouse'),
    path('product-store/', views.getProductStores, name='product-store'),
    path('add-product-to-cart/', views.addProductToShoppingCart, name='add-product-to-cart'),
    path('get-cart/', views.getShoppingCart, name='get-cart'),
    path('delete-cart/', views.deleteCart, name='delete-cart'),
    path('add-order/', views.addOrder, name='add-order'),
    path('store_list/', views.getStoresList, name='store_list'),
    path('store/', views.getStore, name='store'),

]

