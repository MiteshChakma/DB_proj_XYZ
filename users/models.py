from django.db import models
from django.contrib.auth.models import AbstractUser
from pymysql import NULL

class User(AbstractUser):
    ADMINISTRATOR = 1
    CUSTOMER = 2
    STAFF = 3

    ROLE_CHOICES = (
        (ADMINISTRATOR, 'Administrator'),
        (CUSTOMER, 'Customer'),
        (STAFF, 'Staff'),
    )

    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=True, null=True, verbose_name="Role")

    location = models.CharField(max_length=100, blank=True, null=True, verbose_name="Location")


class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer_profile', verbose_name="User")
    shipping_address = models.TextField(blank=True, null=True, verbose_name="Shipping Address")
    billing_address = models.TextField(blank=True, null=True, verbose_name="Billing Address")
    preferred_payment_method = models.CharField(max_length=100, blank=True, null=True, verbose_name="Preferred Payment Method")
    preferred_shipping_method = models.CharField(max_length=100, blank=True, null=True, verbose_name="Preferred Shipping Method")


class Product(models.Model):
    pID = models.IntegerField(verbose_name="id",null=True)
    name = models.CharField(max_length=1024, verbose_name="Product Name")
    price = models.IntegerField(verbose_name="Product Price")
    rating = models.IntegerField(verbose_name="Product Rating")
    review = models.TextField(verbose_name="Product Review")

class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Customer")


class ProductOrder(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="order")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="producto")
    amount = models.IntegerField(verbose_name="amounto",null=True)


class Cart(models.Model):
    customer = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Customer")


class ProductCart(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart', verbose_name="cart")
    product = models.ForeignKey(Product,on_delete=models.CASCADE, related_name='productc',default=0, verbose_name="productc")
    amount = models.IntegerField(verbose_name="amountc",null=True)

class Warehouse(models.Model):
    name = models.CharField(max_length=1024, verbose_name="Product Name")

class ProductWarehouse(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='productw', verbose_name="product")
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='pwarehouse', verbose_name="warehouse")
    productAmount = models.IntegerField(verbose_name="name",null=True)

    
class Store(models.Model):
    warehouse = models.OneToOneField(Warehouse, on_delete=models.CASCADE, related_name='warehouse', verbose_name="Warehouse")
    address = models.CharField(max_length=100, blank=True, null=True, verbose_name="City")
    review = models.TextField(verbose_name="Review")
    rating = models.IntegerField(verbose_name="Rating")


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses', verbose_name="User")
    address_type = models.CharField(max_length=10, choices=[('shipping', 'Shipping'), ('billing', 'Billing')], verbose_name="Address Type")
    street = models.CharField(max_length=1024, verbose_name="Street")
    city = models.CharField(max_length=512, verbose_name="City")
    state = models.CharField(max_length=512, verbose_name="State")
    zip_code = models.CharField(max_length=20, verbose_name="Zip Code")
    country = models.CharField(max_length=50, verbose_name="Country")


class StaffProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='staff_profile', verbose_name="User")
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='store', verbose_name="Store")
    rating = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True, verbose_name="Staff Rating")
