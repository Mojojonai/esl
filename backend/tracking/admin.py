from django.contrib import admin
from .models import UserProgress, Badge, UserBadge, ReviewItem


@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'get_level_unit', 'skill_area', 'progress_percent', 'average_score']
    list_filter = ['level', 'unit', 'skill_area', 'updated_at']
    search_fields = ['user__username']
    readonly_fields = ['updated_at']
    
    def get_level_unit(self, obj):
        return f"{obj.level.code} - Unit {obj.unit.order}"
    get_level_unit.short_description = 'Level & Unit'


@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'icon_url']
    search_fields = ['name', 'code']
    fieldsets = (
        ('Badge Information', {'fields': ('code', 'name', 'description')}),
        ('Display', {'fields': ('icon_url',)}),
        ('Condition', {'fields': ('condition',)}),
    )


@admin.register(UserBadge)
class UserBadgeAdmin(admin.ModelAdmin):
    list_display = ['user', 'badge', 'earned_at']
    list_filter = ['badge', 'earned_at']
    search_fields = ['user__username', 'badge__name']
    readonly_fields = ['earned_at']


@admin.register(ReviewItem)
class ReviewItemAdmin(admin.ModelAdmin):
    list_display = ['user', 'exercise_title', 'strength_score', 'next_review_date', 'mistake_count']
    list_filter = ['strength_score', 'next_review_date', 'created_at']
    search_fields = ['user__username', 'exercise__title']
    readonly_fields = ['created_at']
    
    def exercise_title(self, obj):
        return obj.exercise.title
    exercise_title.short_description = 'Exercise'
