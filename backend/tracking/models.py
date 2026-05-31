from django.db import models
from django.contrib.auth.models import User
from learning.models import Level, Unit, SkillArea, Exercise


class UserProgress(models.Model):
    """
    Track overall user progress by level, unit, and skill
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='progress')
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    skill_area = models.ForeignKey(SkillArea, on_delete=models.CASCADE)
    progress_percent = models.IntegerField(default=0)  # 0-100
    completed_exercises = models.IntegerField(default=0)
    total_exercises = models.IntegerField(default=0)
    average_score = models.FloatField(default=0.0)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['user', 'level', 'unit', 'skill_area']
        verbose_name_plural = "User Progress"
    
    def __str__(self):
        return f"{self.user.username} - {self.level.code} Unit {self.unit.order} - {self.skill_area.name}"


class Badge(models.Model):
    """
    Badge definitions for achievements
    """
    BADGE_TYPES = [
        ('first_steps', 'First Steps'),
        ('listening_hero', 'Listening Hero'),
        ('word_builder', 'Word Builder'),
        ('sentence_master', 'Sentence Master'),
        ('comprehension_star', 'Comprehension Star'),
        ('streak_keeper', 'Streak Keeper'),
        ('unit_completer', 'Unit Completer'),
        ('skill_master', 'Skill Master'),
        ('memory_champion', 'Memory Champion'),
        ('brave_speaker', 'Brave Speaker'),
    ]
    
    code = models.CharField(max_length=50, unique=True, choices=BADGE_TYPES)
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon_url = models.URLField(blank=True)
    condition = models.JSONField()  # e.g., {"type": "xp_threshold", "value": 100}
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Badges"


class UserBadge(models.Model):
    """
    Track user's earned badges
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='badges')
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    earned_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'badge']
        verbose_name_plural = "User Badges"
    
    def __str__(self):
        return f"{self.user.username} - {self.badge.name}"


class ReviewItem(models.Model):
    """
    Spaced repetition review items for memory strengthening
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='review_items')
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    next_review_date = models.DateField()  # When this should be reviewed next
    strength_score = models.IntegerField(default=0)  # 0-3 (0=weak, 3=strong)
    mistake_count = models.IntegerField(default=0)
    last_reviewed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'exercise']
        verbose_name_plural = "Review Items"
        ordering = ['next_review_date']
    
    def __str__(self):
        return f"{self.user.username} - {self.exercise.title}"
