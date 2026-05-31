from django.contrib import admin
from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['username', 'current_level', 'current_unit', 'xp', 'streak', 'last_login_date']
    list_filter = ['current_level', 'created_at']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Learning Progress', {
            'fields': ('current_level', 'current_unit', 'xp', 'streak')
        }),
        ('Account Status', {
            'fields': ('first_login', 'password_changed', 'last_login_date')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    def username(self, obj):
        return obj.user.username
    username.short_description = 'Username'
