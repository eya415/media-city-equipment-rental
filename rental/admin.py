from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils.html import format_html
from .models import (Product, Category, Brand, WishlistItem,
                    Order, OrderItem, IndividualProfile,
                    CorporateProfile, StudioProfile)

class ReadOnlyAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return [field.name for field in obj._meta.fields]
        return []

# Custom User Admin
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 
                   'is_staff', 'get_profile_type', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups', 'date_joined')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    
    def get_profile_type(self, obj):
        if hasattr(obj, 'individualprofile'):
            return "Individual"
        elif hasattr(obj, 'corporateprofile'):
            return "Corporate"
        elif hasattr(obj, 'studioprofile'):
            return "Studio"
        return "No Profile"
    get_profile_type.short_description = 'Profile Type'

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# Profile Admin Classes
@admin.register(IndividualProfile)
class IndividualProfileAdmin(ReadOnlyAdmin):
    list_display = ('user', 'full_name', 'date_of_birth', 'mobile_phone', 
                   'governorate', 'city', 'hear_about', 'created_at')
    search_fields = ('user__username', 'full_name', 'mobile_phone')
    list_filter = ('governorate', 'city', 'hear_about', 'created_at')
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('user', 'full_name', 'date_of_birth', 'professional_category', 'portfolio_link')
        }),
        ('Contact Information', {
            'fields': ('mobile_phone', 'whatsapp_number', 'profile_link')
        }),
        ('Location', {
            'fields': ('governorate', 'city', 'street', 'building', 'floor', 'apartment')
        }),
        ('Documents', {
            'fields': ('id_front', 'id_rear', 'other_id')
        }),
        ('Metadata', {
            'fields': ('hear_about', 'created_at')
        })
    )
    
    def id_front(self, obj):
        if obj.id_front:
            return format_html('<a href="{}" target="_blank">{}</a>', obj.id_front.url, obj.id_front.name)
        return "-"
    id_front.short_description = 'ID Front'

    def id_rear(self, obj):
        if obj.id_rear:
            return format_html('<a href="{}" target="_blank">{}</a>', obj.id_rear.url, obj.id_rear.name)
        return "-"
    id_rear.short_description = 'ID Back'

@admin.register(CorporateProfile)
class CorporateProfileAdmin(ReadOnlyAdmin):
    list_display = ('user', 'company_name', 'ceo_phone', 'company_website',
                   'governorate', 'city', 'created_at')
    search_fields = ('user__username', 'company_name', 'ceo_phone', 'company_website')
    list_filter = ('governorate', 'city', 'created_at')
    
    fieldsets = (
        ('Company Information', {
            'fields': ('user', 'company_name', 'company_address', 'company_website', 'company_social')
        }),
        ('CEO Information', {
            'fields': ('ceo_name', 'ceo_phone', 'ceo_email')
        }),
        ('Authorized Person', {
            'fields': ('authorized_name', 'authorized_phone', 'authorized_email')
        }),
        ('Location', {
            'fields': ('governorate', 'city', 'street', 'building', 'floor', 'apartment')
        }),
        ('Documents', {
            'fields': ('ceo_id_front', 'ceo_id_rear', 'authorized_id_front', 
                      'authorized_id_rear', 'tax_certificate', 'commercial_registration')
        }),
        ('Metadata', {
            'fields': ('hear_about', 'created_at')
        })
    )

@admin.register(StudioProfile)
class StudioProfileAdmin(ReadOnlyAdmin):
    list_display = ('user', 'studio_name', 'phone', 'email',
                   'governorate', 'city', 'created_at')
    search_fields = ('user__username', 'studio_name', 'phone', 'email')
    list_filter = ('governorate', 'city', 'created_at')
    
    fieldsets = (
        ('Studio Information', {
            'fields': ('user', 'studio_name', 'phone', 'whatsapp', 'email')
        }),
        ('Location', {
            'fields': ('governorate', 'city', 'street', 'building', 'floor', 'apartment')
        }),
        ('Documents', {
            'fields': ('commercial_register', 'tax_card')
        }),
        ('Metadata', {
            'fields': ('hear_about', 'created_at')
        })
    )

# [Keep the rest of your Product, Category, Brand, WishlistItem, Order admin classes unchanged]

# Product Admin Classes
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'category', 'price')
    search_fields = ('name', 'description')
    list_filter = ('brand', 'category')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon_class')
    search_fields = ('name',)

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'logo')
    search_fields = ('name',)

@admin.register(WishlistItem)
class WishlistItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'added_at')
    list_filter = ('user', 'added_at')
    search_fields = ('product__name', 'user__username')

# Order Admin Classes
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'quantity', 'price')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'start_date', 'end_date',
                   'is_delivery', 'total_price', 'status', 'created_at')
    list_filter = ('is_delivery', 'status', 'created_at')
    search_fields = ('user__username', 'delivery_name')
    readonly_fields = ('created_at',)
    inlines = [OrderItemInline]