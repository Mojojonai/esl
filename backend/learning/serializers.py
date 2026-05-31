from rest_framework import serializers
from .models import (
    Level, Unit, Lesson, SkillArea, VocabularyItem, Dialogue, DialogueLine,
    Exercise, Game, UserExerciseAttempt, UserGameAttempt
)


class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = ['id', 'code', 'name', 'description', 'order', 'is_active']
        read_only_fields = ['id']


class SkillAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SkillArea
        fields = ['id', 'name', 'code', 'description', 'icon_name']
        read_only_fields = ['id']


class VocabularyItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = VocabularyItem
        fields = [
            'id', 'lesson', 'word', 'part_of_speech', 'example_sentence',
            'image_url', 'audio_url', 'difficulty'
        ]
        read_only_fields = ['id']


class DialogueLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = DialogueLine
        fields = ['id', 'speaker', 'text', 'audio_url', 'order']
        read_only_fields = ['id']


class DialogueSerializer(serializers.ModelSerializer):
    lines = DialogueLineSerializer(many=True, read_only=True)
    
    class Meta:
        model = Dialogue
        fields = ['id', 'lesson', 'title', 'context', 'audio_url', 'speakers', 'lines']
        read_only_fields = ['id']


class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = [
            'id', 'lesson', 'skill_area', 'exercise_type', 'title',
            'instruction', 'content', 'hints', 'xp_reward', 'order', 'is_active'
        ]
        read_only_fields = ['id']
    
    def to_representation(self, instance):
        """Hide correct_answer from non-admin users when not submitted."""
        data = super().to_representation(instance)
        # Don't show correct answer unless explicitly asked
        # This is handled in views with a detail_correct_answer action
        return data


class ExerciseDetailSerializer(ExerciseSerializer):
    """For admin only - includes correct answer"""
    class Meta:
        model = Exercise
        fields = [
            'id', 'lesson', 'skill_area', 'exercise_type', 'title',
            'instruction', 'content', 'correct_answer', 'hints', 'xp_reward', 'order'
        ]
        read_only_fields = ['id']


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ['id', 'lesson', 'game_type', 'title', 'description', 'config', 'xp_reward', 'order']
        read_only_fields = ['id']


class UserExerciseAttemptSerializer(serializers.ModelSerializer):
    exercise_title = serializers.CharField(source='exercise.title', read_only=True)
    
    class Meta:
        model = UserExerciseAttempt
        fields = [
            'id', 'user', 'exercise', 'exercise_title', 'answer', 'score',
            'max_score', 'completed', 'mistakes', 'time_spent_seconds', 'created_at'
        ]
        read_only_fields = ['id', 'user', 'created_at']


class UserGameAttemptSerializer(serializers.ModelSerializer):
    game_title = serializers.CharField(source='game.title', read_only=True)
    
    class Meta:
        model = UserGameAttempt
        fields = [
            'id', 'user', 'game', 'game_title', 'score', 'completed',
            'time_spent_seconds', 'created_at'
        ]
        read_only_fields = ['id', 'user', 'created_at']


class LessonSerializer(serializers.ModelSerializer):
    vocabulary = VocabularyItemSerializer(many=True, read_only=True)
    dialogues = DialogueSerializer(many=True, read_only=True)
    
    class Meta:
        model = Lesson
        fields = [
            'id', 'unit', 'title', 'objective', 'grammar_focus',
            'vocabulary_focus', 'order', 'is_active', 'vocabulary', 'dialogues'
        ]
        read_only_fields = ['id']


class UnitSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    
    class Meta:
        model = Unit
        fields = ['id', 'level', 'title', 'description', 'theme', 'order', 'is_active', 'lessons']
        read_only_fields = ['id']


class LevelDetailSerializer(LevelSerializer):
    units = UnitSerializer(many=True, read_only=True)
    
    class Meta:
        model = Level
        fields = ['id', 'code', 'name', 'description', 'order', 'is_active', 'units']
        read_only_fields = ['id']
