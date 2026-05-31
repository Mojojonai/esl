from django.contrib import admin
from .models import GameTemplate


@admin.register(GameTemplate)
class GameTemplateAdmin(admin.ModelAdmin):
    list_display = ['game_type', 'title']
    search_fields = ['title', 'game_type']
    fieldsets = (
        ('Game Information', {'fields': ('game_type', 'title', 'description')}),
        ('Configuration', {'fields': ('default_config',)}),
    )
