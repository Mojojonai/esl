from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from .models import UserProgress, Badge, UserBadge, ReviewItem
from .serializers import (
    UserProgressSerializer, BadgeSerializer, UserBadgeSerializer, ReviewItemSerializer
)


class UserProgressViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for user progress tracking."""
    queryset = UserProgress.objects.all()
    serializer_class = UserProgressSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['level', 'unit', 'skill_area']
    ordering_fields = ['unit__order', 'updated_at']
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return UserProgress.objects.all()
        return UserProgress.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def my_progress(self, request):
        """Get current user's progress."""
        progress = UserProgress.objects.filter(user=request.user)
        serializer = self.get_serializer(progress, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_level(self, request):
        """Get progress by level."""
        level = request.query_params.get('level')
        if not level:
            return Response(
                {'detail': 'Level required.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        progress = UserProgress.objects.filter(
            user=request.user, level__code=level
        )
        serializer = self.get_serializer(progress, many=True)
        return Response(serializer.data)


class UserBadgeViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for user badges."""
    queryset = UserBadge.objects.all()
    serializer_class = UserBadgeSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [OrderingFilter]
    ordering_fields = ['earned_at']
    ordering = ['-earned_at']
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return UserBadge.objects.all()
        return UserBadge.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def my_badges(self, request):
        """Get current user's earned badges."""
        badges = UserBadge.objects.filter(user=request.user).order_by('-earned_at')
        serializer = self.get_serializer(badges, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def available(self, request):
        """Get all available badges."""
        badges = Badge.objects.all()
        serializer = BadgeSerializer(badges, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def check_achievements(self, request):
        """Check and award badges based on current progress."""
        user = request.user
        profile = user.profile
        awarded_badges = []
        
        # First Steps Badge: Complete first exercise
        if UserBadge.objects.filter(user=user).exists() == False:
            from learning.models import UserExerciseAttempt
            if UserExerciseAttempt.objects.filter(user=user).exists():
                badge = Badge.objects.get(code='first_steps')
                user_badge, created = UserBadge.objects.get_or_create(user=user, badge=badge)
                if created:
                    awarded_badges.append(badge.name)
        
        # XP Threshold Badges
        xp_milestones = {
            'word_builder': 50,
            'sentence_master': 100,
            'memory_champion': 200,
        }
        
        for badge_code, xp_threshold in xp_milestones.items():
            if profile.xp >= xp_threshold:
                badge = Badge.objects.get(code=badge_code)
                user_badge, created = UserBadge.objects.get_or_create(user=user, badge=badge)
                if created:
                    awarded_badges.append(badge.name)
        
        # Streak Badge
        if profile.streak >= 7:
            badge = Badge.objects.get(code='streak_keeper')
            user_badge, created = UserBadge.objects.get_or_create(user=user, badge=badge)
            if created:
                awarded_badges.append(badge.name)
        
        badges = UserBadge.objects.filter(user=user)
        serializer = self.get_serializer(badges, many=True)
        
        return Response({
            'all_badges': serializer.data,
            'newly_awarded': awarded_badges,
            'total_badges': badges.count(),
        })


class ReviewItemViewSet(viewsets.ModelViewSet):
    """ViewSet for spaced repetition review items."""
    queryset = ReviewItem.objects.all()
    serializer_class = ReviewItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['exercise__skill_area']
    ordering_fields = ['next_review_date', 'strength_score']
    ordering = ['next_review_date']
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return ReviewItem.objects.all()
        return ReviewItem.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def due_for_review(self, request):
        """Get exercises due for review today."""
        today = timezone.now().date()
        items = ReviewItem.objects.filter(
            user=request.user,
            next_review_date__lte=today
        ).order_by('strength_score', 'next_review_date')
        
        serializer = self.get_serializer(items, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def mark_correct(self, request, pk=None):
        """Mark a review item as correct."""
        item = self.get_object()
        
        if item.user != request.user and not request.user.is_staff:
            return Response(
                {'detail': 'Permission denied.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Increase strength score
        item.strength_score = min(item.strength_score + 1, 3)
        
        # Schedule next review based on strength
        review_intervals = {
            0: 1,    # 1 day
            1: 2,    # 2 days
            2: 5,    # 5 days
            3: 10,   # 10 days
        }
        days_until_next = review_intervals.get(item.strength_score, 10)
        item.next_review_date = timezone.now().date() + timedelta(days=days_until_next)
        item.last_reviewed_at = timezone.now()
        item.save()
        
        serializer = self.get_serializer(item)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def mark_incorrect(self, request, pk=None):
        """Mark a review item as incorrect."""
        item = self.get_object()
        
        if item.user != request.user and not request.user.is_staff:
            return Response(
                {'detail': 'Permission denied.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Reset strength score and schedule for tomorrow
        item.strength_score = max(item.strength_score - 1, 0)
        item.mistake_count += 1
        item.next_review_date = timezone.now().date() + timedelta(days=1)
        item.last_reviewed_at = timezone.now()
        item.save()
        
        serializer = self.get_serializer(item)
        return Response(serializer.data)
