from django.db import models


class GameTemplate(models.Model):
    """
    Pre-configured game templates for different game types
    """
    GAME_TYPES = [
        ('memory_match', 'Memory Match'),
        ('sound_match', 'Sound Match'),
        ('sentence_race', 'Sentence Race'),
        ('vocabulary_hunt', 'Vocabulary Treasure Hunt'),
    ]
    
    game_type = models.CharField(max_length=50, choices=GAME_TYPES, unique=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    default_config = models.JSONField()  # Default configuration for this game type
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
