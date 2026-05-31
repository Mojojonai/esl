from django.contrib import admin
from .models import (
    Level, Unit, Lesson, SkillArea, VocabularyItem, Dialogue, DialogueLine,
    Exercise, Game, UserExerciseAttempt, UserGameAttempt
)


@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'order', 'is_active']
    list_filter = ['is_active', 'created_at']
    search_fields = ['code', 'name']
    fieldsets = (
        ('Level Information', {'fields': ('code', 'name', 'description')}),
        ('Settings', {'fields': ('order', 'is_active')}),
    )


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ['get_level_code', 'order', 'title', 'is_active']
    list_filter = ['level', 'is_active', 'created_at']
    search_fields = ['title', 'theme']
    fieldsets = (
        ('Unit Information', {'fields': ('level', 'title', 'description', 'theme')}),
        ('Settings', {'fields': ('order', 'is_active')}),
    )
    
    def get_level_code(self, obj):
        return obj.level.code
    get_level_code.short_description = 'Level'


@admin.register(SkillArea)
class SkillAreaAdmin(admin.ModelAdmin):
    list_display = ['name', 'code']
    search_fields = ['name', 'code']


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['get_unit_level', 'title', 'order', 'is_active']
    list_filter = ['unit__level', 'is_active', 'created_at']
    search_fields = ['title', 'objective']
    fieldsets = (
        ('Lesson Information', {'fields': ('unit', 'title', 'objective')}),
        ('Focus Areas', {'fields': ('grammar_focus', 'vocabulary_focus')}),
        ('Settings', {'fields': ('order', 'is_active')}),
    )
    
    def get_unit_level(self, obj):
        return f"{obj.unit.level.code} - Unit {obj.unit.order}"
    get_unit_level.short_description = 'Unit'


class DialogueLineInline(admin.TabularInline):
    model = DialogueLine
    extra = 1
    fields = ['speaker', 'text', 'audio_url', 'order']


@admin.register(Dialogue)
class DialogueAdmin(admin.ModelAdmin):
    list_display = ['title', 'get_lesson_unit', 'get_context_preview']
    list_filter = ['lesson__unit__level', 'created_at']
    search_fields = ['title', 'context']
    inlines = [DialogueLineInline]
    fieldsets = (
        ('Dialogue Information', {'fields': ('lesson', 'title', 'context')}),
        ('Media', {'fields': ('audio_url', 'speakers')}),
    )
    
    def get_lesson_unit(self, obj):
        return f"{obj.lesson.unit.level.code} - Unit {obj.lesson.unit.order}"
    get_lesson_unit.short_description = 'Unit'
    
    def get_context_preview(self, obj):
        return obj.context[:50] + '...' if len(obj.context) > 50 else obj.context
    get_context_preview.short_description = 'Context'


@admin.register(VocabularyItem)
class VocabularyItemAdmin(admin.ModelAdmin):
    list_display = ['word', 'get_lesson_title', 'difficulty', 'part_of_speech']
    list_filter = ['lesson__unit__level', 'difficulty', 'created_at']
    search_fields = ['word', 'example_sentence']
    fieldsets = (
        ('Vocabulary Information', {'fields': ('lesson', 'word', 'part_of_speech', 'difficulty')}),
        ('Content', {'fields': ('example_sentence',)}),
        ('Media', {'fields': ('image_url', 'audio_url')}),
    )
    
    def get_lesson_title(self, obj):
        return obj.lesson.title
    get_lesson_title.short_description = 'Lesson'


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ['title', 'get_lesson_unit', 'exercise_type', 'skill_area', 'xp_reward', 'is_active']
    list_filter = ['skill_area', 'exercise_type', 'lesson__unit__level', 'is_active', 'created_at']
    search_fields = ['title', 'instruction']
    fieldsets = (
        ('Exercise Information', {
            'fields': ('lesson', 'title', 'exercise_type', 'skill_area', 'instruction')
        }),
        ('Content', {
            'fields': ('content', 'correct_answer', 'hints')
        }),
        ('Settings', {
            'fields': ('xp_reward', 'order', 'is_active')
        }),
    )
    
    def get_lesson_unit(self, obj):
        return f"{obj.lesson.unit.level.code} - Unit {obj.lesson.unit.order}"
    get_lesson_unit.short_description = 'Unit'


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ['title', 'get_lesson_unit', 'game_type', 'xp_reward', 'is_active']
    list_filter = ['game_type', 'lesson__unit__level', 'is_active', 'created_at']
    search_fields = ['title', 'description']
    fieldsets = (
        ('Game Information', {
            'fields': ('lesson', 'title', 'description', 'game_type')
        }),
        ('Configuration', {
            'fields': ('config',)
        }),
        ('Settings', {
            'fields': ('xp_reward', 'order', 'is_active')
        }),
    )
    
    def get_lesson_unit(self, obj):
        return f"{obj.lesson.unit.level.code} - Unit {obj.lesson.unit.order}"
    get_lesson_unit.short_description = 'Unit'


@admin.register(UserExerciseAttempt)
class UserExerciseAttemptAdmin(admin.ModelAdmin):
    list_display = ['user', 'exercise_title', 'score', 'completed', 'created_at']
    list_filter = ['completed', 'score', 'created_at', 'exercise__lesson__unit__level']
    search_fields = ['user__username', 'exercise__title']
    readonly_fields = ['user', 'exercise', 'answer', 'created_at', 'updated_at']
    
    def exercise_title(self, obj):
        return obj.exercise.title
    exercise_title.short_description = 'Exercise'


@admin.register(UserGameAttempt)
class UserGameAttemptAdmin(admin.ModelAdmin):
    list_display = ['user', 'game_title', 'score', 'completed', 'created_at']
    list_filter = ['completed', 'created_at', 'game__lesson__unit__level']
    search_fields = ['user__username', 'game__title']
    readonly_fields = ['user', 'game', 'created_at']
    
    def game_title(self, obj):
        return obj.game.title
    game_title.short_description = 'Game'
