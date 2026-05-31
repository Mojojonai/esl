from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class UserProfile(models.Model):
    """Extended user profile for learning progress."""
    
    LEVEL_CHOICES = [
        ('A1', 'Beginner'),
        ('A2', 'Elementary'),
        ('B1', 'Intermediate'),
        ('B2', 'Upper Intermediate'),
        ('C1', 'Advanced'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    current_level = models.CharField(max_length=2, choices=LEVEL_CHOICES, default='A1')
    current_unit = models.IntegerField(default=1)
    xp = models.IntegerField(default=0)
    streak = models.IntegerField(default=0)
    last_login_date = models.DateTimeField(null=True, blank=True)
    first_login = models.BooleanField(default=True)
    password_changed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.current_level}"
    
    class Meta:
        verbose_name_plural = "User Profiles"
