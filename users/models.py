from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ADMINISTRATOR = 1
    CUSTOMER = 2
    CUSTOMER_SERVICE = 3
    DB_ADMINISTRATOR = 4

    ROLE_CHOICES = (
        (ADMINISTRATOR, 'Administrator'),
        (CUSTOMER, 'Customer'),
        (CUSTOMER_SERVICE, 'Customer Service'),
        (DB_ADMINISTRATOR, 'Database Administrator'),
    )

    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=True, null=True, verbose_name="Role")

    location = models.CharField(max_length=100, blank=True, null=True, verbose_name="Location")

    def is_administrator(self):
        return self.role == self.ADMINISTRATOR

    def is_customer(self):
        return self.role == self.CUSTOMER

    def is_customer_service(self):
        return self.role == self.CUSTOMER_SERVICE

    def is_db_administrator(self):
        return self.role == self.DB_ADMINISTRATOR

    def __str__(self):
        return self.username


class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer_profile', verbose_name="User")
    shipping_address = models.TextField(blank=True, null=True, verbose_name="Shipping Address")
    billing_address = models.TextField(blank=True, null=True, verbose_name="Billing Address")
    preferred_payment_method = models.CharField(max_length=100, blank=True, null=True, verbose_name="Preferred Payment Method")
    preferred_shipping_method = models.CharField(max_length=100, blank=True, null=True, verbose_name="Preferred Shipping Method")

    def __str__(self):
        return f"{self.user.username}'s Profile"


class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Customer")
    # additional fields like order date, status, total price, etc.
    # ...

    def __str__(self):
        return f"Order #{self.pk} by {self.customer.username}"


class Cart(models.Model):
    customer = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Customer")
    # fields for items in the cart
    # ...

    def __str__(self):
        return f"{self.customer.username}'s Cart"


class Wishlist(models.Model):
    customer = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Customer")
    # fields for wishlist items
    # ...

    def __str__(self):
        return f"{self.customer.username}'s Wishlist"


class Review(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Customer")
    # product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Uncomment and use when Product model is defined
    review = models.TextField(verbose_name="Review")
    rating = models.IntegerField(verbose_name="Rating")
    # additional fields 
    # ...

    def __str__(self):
        return f"Review by {self.customer.username}"


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses', verbose_name="User")
    address_type = models.CharField(max_length=10, choices=[('shipping', 'Shipping'), ('billing', 'Billing')], verbose_name="Address Type")
    street = models.CharField(max_length=1024, verbose_name="Street")
    city = models.CharField(max_length=512, verbose_name="City")
    state = models.CharField(max_length=512, verbose_name="State")
    zip_code = models.CharField(max_length=20, verbose_name="Zip Code")
    country = models.CharField(max_length=50, verbose_name="Country")

    def __str__(self):
        return f"{self.user.username} - {self.get_address_type_display()} Address"


class CustomerServiceProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer_service_profile', verbose_name="User")
    service_area = models.CharField(max_length=100, blank=True, null=True, verbose_name="Service Area")
    service_rating = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True, verbose_name="Service Rating")

    def __str__(self):
        return f"{self.user.username}'s Service Profile"


class DatabaseAdministratorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='db_administrator_profile', verbose_name="User")
    specialization = models.CharField(max_length=100, blank=True, null=True, verbose_name="Specialization")
    access_level = models.CharField(max_length=100, blank=True, null=True, verbose_name="Access Level")

    def __str__(self):
        return f"{self.user.username} - DB Administrator"
