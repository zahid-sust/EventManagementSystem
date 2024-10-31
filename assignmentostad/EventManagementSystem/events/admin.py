from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Event, Category

# --- Custom User Admin Configuration ---

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'role']
    list_filter = ['role', 'is_staff']
    
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role', 'phone_number')}),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('role', 'phone_number')}),
    )

# Register CustomUser model
admin.site.register(CustomUser, CustomUserAdmin)

# --- Event Admin Configuration ---

class EventAdmin(admin.ModelAdmin):
    list_display = ['name', 'date', 'location', 'category', 'created_by', 'max_capacity', 'booked_count']
    list_filter = ['category', 'date']
    search_fields = ['name', 'location']
    ordering = ['date']

# Register Event model
admin.site.register(Event, EventAdmin)

# --- Register Category model ---
admin.site.register(Category)
