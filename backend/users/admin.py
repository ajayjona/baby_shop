from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, VendorProfile

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'user_type', 'is_verified', 'is_active', 'created_at')
    list_filter = ('user_type', 'is_verified', 'is_active', 'is_staff')
    search_fields = ('username', 'email', 'phone_number')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal Info', {'fields': ('user_type', 'phone_number', 'date_of_birth', 'profile_picture')}),
        ('Address', {'fields': ('address_line_1', 'address_line_2', 'city', 'state', 'postal_code', 'country')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_verified', 'groups', 'user_permissions')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'user_type', 'phone_number', 'is_active', 'is_verified'),
        }),
    )
    readonly_fields = ('created_at', 'updated_at')

@admin.register(VendorProfile)
class VendorProfileAdmin(admin.ModelAdmin):
    list_display = ('business_name', 'user', 'is_verified', 'is_active', 'average_rating', 'created_at')
    list_filter = ('is_verified', 'is_active')
    search_fields = ('business_name', 'user__username', 'business_email', 'tax_id')
    fieldsets = (
        (None, {'fields': ('user', 'business_name', 'business_description')}),
        ('Business Details', {'fields': ('business_license', 'tax_id', 'business_phone', 'business_email', 'website', 'business_address')}),
        ('Verification', {'fields': ('is_verified', 'verification_date', 'is_active')}),
        ('Ratings', {'fields': ('average_rating', 'total_reviews')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )
    readonly_fields = ('created_at', 'updated_at', 'average_rating', 'total_reviews')