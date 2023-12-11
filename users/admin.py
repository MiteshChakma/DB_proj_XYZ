from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, CustomerProfile, Order, Cart, Wishlist, Review, Address, StaffProfile, DatabaseAdministratorProfile

# Customizing the UserAdmin to include our new fields
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['username', 'email', 'role', 'is_active']
    list_filter = ['role', 'is_active']
    fieldsets = UserAdmin.fieldsets + (
            (None, {'fields': ('role',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
            (None, {'fields': ('role',)}),
    )

# Admin for CustomerProfile
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'shipping_address', 'billing_address', 'preferred_payment_method', 'preferred_shipping_method']
    search_fields = ['user__username', 'user__email']
    list_filter = ['preferred_payment_method', 'preferred_shipping_method']

# Admin for StaffProfile
class StaffProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'store', 'rating']
    search_fields = ['user__username']
    list_filter = ['store']

# Admin for DatabaseAdministratorProfile
class DatabaseAdministratorProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'specialization', 'access_level']
    search_fields = ['user__username']
    list_filter = ['specialization']

# Admin for Address
class AddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'address_type', 'street', 'city', 'state', 'zip_code', 'country']
    search_fields = ['user__username', 'street', 'city', 'state', 'zip_code', 'country']
    list_filter = ['address_type', 'country']

# Registering models with their respective admin classes
admin.site.register(User, CustomUserAdmin)
admin.site.register(CustomerProfile, CustomerProfileAdmin)
admin.site.register(StaffProfile, StaffProfileAdmin)
admin.site.register(DatabaseAdministratorProfile, DatabaseAdministratorProfileAdmin)
admin.site.register(Address, AddressAdmin)

# Register other models as needed
admin.site.register(Order)
admin.site.register(Cart)
admin.site.register(Wishlist)
admin.site.register(Review)
