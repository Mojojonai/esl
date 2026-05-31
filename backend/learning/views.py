from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Avg, Count
from django.utils import timezone
from datetime import timedelta
from .models import (
    Level, Unit, Lesson, SkillArea, VocabularyItem, Dialogue,
    Exercise, Game, UserExerciseAttempt, UserGameAttempt
)
from tracking.models import UserProgress, ReviewItem
from .serializers import (
    LevelSerializer, LevelDetailSerializer, UnitSerializer, LessonSerializer,
    SkillAreaSerializer, VocabularyItemSerializer, DialogueSerializer,
    ExerciseSerializer, ExerciseDetailSerializer, GameSerializer,
    UserExerciseAttemptSerializer, UserGameAttemptSerializer
)


class LevelViewSet(viewsets.ModelViewSet):
    """ViewSet for learning levels (A1, A2, B1, B2, C1)."""
    queryset = Level.objects.filter(is_active=True).order_by('order')
    serializer_class = LevelSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return LevelDetailSerializer
        return LevelSerializer


class UnitViewSet(viewsets.ModelViewSet):
    """ViewSet for learning units."""
    queryset = Unit.objects.filter(is_active=True).order_by('level', 'order')
    serializer_class = UnitSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['level']
    ordering_fields = ['order', 'created_at']
    ordering = ['order']
    
    @action(detail=False, methods=['get'])
    def by_level(self, request):
        """Get units by level code."""
        level_code = request.query_params.get('level')
        if not level_code:
            return Response({'detail': 'Level code required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        units = Unit.objects.filter(level__code=level_code, is_active=True).order_by('order')
        serializer = self.get_serializer(units, many=True)
        return Response(serializer.data)


class LessonViewSet(viewsets.ModelViewSet):
    """ViewSet for lessons."""
    queryset = Lesson.objects.filter(is_active=True).order_by('unit', 'order')
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['unit', 'unit__level']
    ordering_fields = ['order', 'created_at']
    ordering = ['order']


class SkillAreaViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for skill areas (Listening, Reading, Writing, etc.)."""
    queryset = SkillArea.objects.all()
    serializer_class = SkillAreaSerializer
    permission_classes = [permissions.IsAuthenticated]


class VocabularyViewSet(viewsets.ModelViewSet):
    """ViewSet for vocabulary items."""
    queryset = VocabularyItem.objects.all().order_by('lesson', 'id')
    serializer_class = VocabularyItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['lesson', 'difficulty']
    search_fields = ['word', 'example_sentence']
    ordering_fields = ['difficulty', 'created_at']


class DialogueViewSet(viewsets.ModelViewSet):
    """ViewSet for dialogues."""
    queryset = Dialogue.objects.all().order_by('lesson')
    serializer_class = DialogueSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['lesson']
    search_fields = ['title', 'context']


class ExerciseViewSet(viewsets.ModelViewSet):
    """ViewSet for exercises."""
    queryset = Exercise.objects.filter(is_active=True).order_by('lesson', 'order')
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['lesson', 'skill_area', 'exercise_type', 'lesson__unit__level']
    search_fields = ['title', 'instruction']
    ordering_fields = ['order', 'xp_reward', 'created_at']
    ordering = ['order']
    
    def get_serializer_class(self):
        if self.action == 'retrieve' and self.request.user.is_staff:
            return ExerciseDetailSerializer
        return ExerciseSerializer
    
    @action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        """Submit an exercise answer."""
        exercise = self.get_object()
        answer = request.data.get('answer')
        time_spent = request.data.get('time_spent_seconds', 0)
        
        if answer is None:
            return Response({'detail': 'Answer required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if answer is correct
        correct_answer = exercise.correct_answer
        is_correct = answer == correct_answer
        
        # Calculate score
        score = 100 if is_correct else 0
        
        # Create attempt record
        attempt = UserExerciseAttempt.objects.create(
            user=request.user,
            exercise=exercise,
            answer=answer,
            score=score,
            completed=True,
            time_spent_seconds=time_spent
        )
        
        # Award XP if correct
        xp_earned = exercise.xp_reward if is_correct else 0
        if is_correct:
            request.user.profile.xp += xp_earned
            request.user.profile.save()

        # Update review item for spaced repetition
        if is_correct:
            try:
                review_item = ReviewItem.objects.get(user=request.user, exercise=exercise)
                review_item.strength_score = min(review_item.strength_score + 1, 3)
                next_interval = {1: 2, 2: 5, 3: 10}.get(review_item.strength_score, 10)
                review_item.next_review_date = timezone.now().date() + timedelta(days=next_interval)
                review_item.last_reviewed_at = timezone.now()
                review_item.save()
            except ReviewItem.DoesNotExist:
                pass
        else:
            review_item, created = ReviewItem.objects.get_or_create(
                user=request.user,
                exercise=exercise,
                defaults={
                    'next_review_date': timezone.now().date() + timedelta(days=1),
                    'strength_score': 0,
                    'mistake_count': 1,
                }
            )
            if not created:
                review_item.mistake_count += 1
                review_item.strength_score = 0
                review_item.next_review_date = timezone.now().date() + timedelta(days=1)
                review_item.last_reviewed_at = timezone.now()
                review_item.save()

        # Update progress for the lesson and skill area
        lesson_unit = exercise.lesson.unit
        completed_exercises = UserExerciseAttempt.objects.filter(
            user=request.user,
            exercise__lesson__unit=lesson_unit,
            exercise__skill_area=exercise.skill_area,
            score__gte=70
        ).values('exercise').distinct().count()

        total_exercises = Exercise.objects.filter(
            lesson__unit=lesson_unit,
            skill_area=exercise.skill_area,
            is_active=True
        ).count()

        average_score = UserExerciseAttempt.objects.filter(
            user=request.user,
            exercise__lesson__unit=lesson_unit,
            exercise__skill_area=exercise.skill_area
        ).aggregate(avg_score=Avg('score'))['avg_score'] or 0

        progress, _ = UserProgress.objects.get_or_create(
            user=request.user,
            level=lesson_unit.level,
            unit=lesson_unit,
            skill_area=exercise.skill_area,
            defaults={
                'completed_exercises': completed_exercises,
                'total_exercises': total_exercises,
                'average_score': average_score,
                'progress_percent': int((completed_exercises / total_exercises) * 100) if total_exercises else 0,
            }
        )
        progress.completed_exercises = completed_exercises
        progress.total_exercises = total_exercises
        progress.average_score = average_score
        progress.progress_percent = int((completed_exercises / total_exercises) * 100) if total_exercises else 0
        progress.save()
        
        serializer = UserExerciseAttemptSerializer(attempt)
        return Response({
            'attempt': serializer.data,
            'is_correct': is_correct,
            'xp_earned': xp_earned,
            'correct_answer': correct_answer if not is_correct else None,
        })
    
    @action(detail=False, methods=['get'])
    def by_lesson(self, request):
        """Get exercises by lesson."""
        lesson_id = request.query_params.get('lesson')
        skill = request.query_params.get('skill')
        
        exercises = Exercise.objects.filter(
            lesson_id=lesson_id, is_active=True
        ).order_by('order')
        
        if skill:
            exercises = exercises.filter(skill_area__code=skill)
        
        serializer = self.get_serializer(exercises, many=True)
        return Response(serializer.data)


class GameViewSet(viewsets.ModelViewSet):
    """ViewSet for mini-games."""
    queryset = Game.objects.filter(is_active=True).order_by('lesson', 'order')
    serializer_class = GameSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['lesson', 'game_type']
    search_fields = ['title']
    ordering_fields = ['order', 'xp_reward']
    ordering = ['order']
    
    @action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        """Submit game attempt."""
        game = self.get_object()
        score = request.data.get('score', 0)
        time_spent = request.data.get('time_spent_seconds', 0)
        
        attempt = UserGameAttempt.objects.create(
            user=request.user,
            game=game,
            score=score,
            completed=True,
            time_spent_seconds=time_spent
        )
        
        # Award XP based on score
        # If score >= 70%, award full XP
        if score >= 70:
            request.user.profile.xp += game.xp_reward
            request.user.profile.save()
            xp_earned = game.xp_reward
        else:
            xp_earned = 0
        
        serializer = UserGameAttemptSerializer(attempt)
        return Response({
            'attempt': serializer.data,
            'xp_earned': xp_earned,
        })
