from rest_framework import serializers
from .models import UserProgress, Badge, UserBadge, ReviewItem
from learning.models import Unit, SkillArea
from learning.serializers import UnitSerializer, SkillAreaSerializer


class BadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Badge
        fields = ['id', 'code', 'name', 'description', 'icon_url', 'condition']
        read_only_fields = ['id']


class UserBadgeSerializer(serializers.ModelSerializer):
    badge = BadgeSerializer(read_only=True)
    
    class Meta:
        model = UserBadge
        fields = ['id', 'user', 'badge', 'earned_at']
        read_only_fields = ['id', 'user', 'earned_at']


class UserProgressSerializer(serializers.ModelSerializer):
    unit_details = UnitSerializer(source='unit', read_only=True)
    skill_details = SkillAreaSerializer(source='skill_area', read_only=True)
    
    class Meta:
        model = UserProgress
        fields = [
            'id', 'user', 'level', 'unit', 'unit_details', 'skill_area', 'skill_details',
            'progress_percent', 'completed_exercises', 'total_exercises', 'average_score'
        ]
        read_only_fields = ['id']


class ReviewItemSerializer(serializers.ModelSerializer):
    exercise_title = serializers.CharField(source='exercise.title', read_only=True)
    exercise_type = serializers.CharField(source='exercise.exercise_type', read_only=True)
    
    class Meta:
        model = ReviewItem
        fields = [
            'id', 'user', 'exercise', 'exercise_title', 'exercise_type',
            'next_review_date', 'strength_score', 'mistake_count', 'last_reviewed_at'
        ]
        read_only_fields = ['id', 'user']
