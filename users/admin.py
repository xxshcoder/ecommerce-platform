from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fields = [
        'phone_number', 'date_of_birth', 'profile_picture', 'bio',
        'address_line1', 'address_line2', 'city', 'state',
        'postal_code', 'country', 'newsletter_subscription'
    ]

class UserAdmin(BaseUserAdmin):
    inlines = [UserProfileInline]
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'date_joined']
    list_filter = ['is_staff', 'is_superuser', 'is_active', 'date_joined']

# Unregister the default User admin and register our custom one
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone_number', 'city', 'country', 'newsletter_subscription']
    list_filter = ['newsletter_subscription', 'country', 'created_at']
    search_fields = ['user__username', 'user__email', 'phone_number', 'city']
    readonly_fields = ['created_at', 'updated_at']