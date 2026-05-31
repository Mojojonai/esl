from django.db import models
from django.contrib.auth.models import User
import json


class Level(models.Model):
    """
    CEFR Language Levels: A1, A2, B1, B2, C1
    """
    LEVEL_CHOICES = [
        ('A1', 'Beginner'),
        ('A2', 'Elementary'),
        ('B1', 'Intermediate'),
        ('B2', 'Upper Intermediate'),
        ('C1', 'Advanced'),
    ]
    
    code = models.CharField(max_length=2, choices=LEVEL_CHOICES, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.code} - {self.name}"


class Unit(models.Model):
    """
    Learning units within a level (e.g., Unit 1, Unit 2, etc.)
    """
    level = models.ForeignKey(Level, on_delete=models.CASCADE, related_name='units')
    title = models.CharField(max_length=200)
    description = models.TextField()
    theme = models.CharField(max_length=200)  # e.g., "Introduction", "Greetings"
    order = models.IntegerField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['level', 'order']
        unique_together = ['level', 'order']
    
    def __str__(self):
        return f"{self.level.code} - Unit {self.order}: {self.title}"


class SkillArea(models.Model):
    """
    Learning skill areas: Listening, Comprehension, Reading, Writing, Speaking
    """
    SKILL_CHOICES = [
        ('listening', 'Listening'),
        ('comprehension', 'Comprehension'),
        ('reading', 'Reading'),
        ('writing', 'Writing'),
        ('speaking', 'Speaking'),
    ]
    
    name = models.CharField(max_length=50, choices=SKILL_CHOICES, unique=True)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField()
    icon_name = models.CharField(max_length=50)  # For UI icons
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Skill Areas"


class Lesson(models.Model):
    """
    Individual lessons within a unit
    """
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    objective = models.TextField()  # What learner will be able to do
    grammar_focus = models.TextField(blank=True)  # e.g., "Present tense of 'to be'"
    vocabulary_focus = models.TextField(blank=True)  # e.g., "Greetings"
    order = models.IntegerField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['unit', 'order']
        unique_together = ['unit', 'order']
    
    def __str__(self):
        return f"{self.unit} - Lesson {self.order}: {self.title}"


class VocabularyItem(models.Model):
    """
    Vocabulary words and phrases for lessons
    """
    DIFFICULTY_CHOICES = [
        (1, 'Easy'),
        (2, 'Medium'),
        (3, 'Hard'),
    ]
    
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='vocabulary')
    word = models.CharField(max_length=200)
    part_of_speech = models.CharField(max_length=50, blank=True)  # noun, verb, adjective, etc.
    example_sentence = models.TextField()
    image_url = models.URLField(blank=True)
    audio_url = models.URLField(blank=True)
    difficulty = models.IntegerField(choices=DIFFICULTY_CHOICES, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.word} - {self.lesson}"
    
    class Meta:
        verbose_name_plural = "Vocabulary Items"


class Dialogue(models.Model):
    """
    Dialogues for listening and comprehension exercises
    """
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='dialogues')
    title = models.CharField(max_length=200)
    context = models.TextField()  # e.g., "Meeting a friend in the morning"
    audio_url = models.URLField(blank=True)
    speakers = models.JSONField(default=list)  # List of character names
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title} - {self.lesson}"
    
    class Meta:
        verbose_name_plural = "Dialogues"


class DialogueLine(models.Model):
    """
    Individual lines in a dialogue
    """
    dialogue = models.ForeignKey(Dialogue, on_delete=models.CASCADE, related_name='lines')
    speaker = models.CharField(max_length=100)
    text = models.TextField()
    audio_url = models.URLField(blank=True)
    order = models.IntegerField()
    
    class Meta:
        ordering = ['dialogue', 'order']
        unique_together = ['dialogue', 'order']
    
    def __str__(self):
        return f"{self.speaker}: {self.text[:50]}"


class Exercise(models.Model):
    """
    Individual exercises within lessons
    """
    EXERCISE_TYPES = [
        # Listening
        ('audio_image_match', 'Audio-Image Match'),
        ('audio_multiple_choice', 'Audio Multiple Choice'),
        ('dictation', 'Dictation'),
        ('dialogue_comprehension', 'Dialogue Comprehension'),
        
        # Comprehension
        ('picture_situation_match', 'Picture Situation Match'),
        ('dialogue_meaning_question', 'Dialogue Meaning Question'),
        ('true_false', 'True/False'),
        ('choose_best_response', 'Choose Best Response'),
        
        # Reading
        ('word_picture_match', 'Word-Picture Match'),
        ('sentence_picture_match', 'Sentence-Picture Match'),
        ('read_along', 'Read-Along with Highlighting'),
        ('vocabulary_in_context', 'Vocabulary in Context'),
        
        # Writing
        ('fill_blank', 'Fill in the Blank'),
        ('word_bank_completion', 'Word Bank Completion'),
        ('drag_drop_sentence', 'Drag-Drop Sentence Builder'),
        ('type_missing_word', 'Type the Missing Word'),
        ('correct_sentence', 'Correct the Sentence'),
        ('picture_prompt_writing', 'Picture Prompt Writing'),
        
        # Speaking (future)
        ('repeat_word', 'Repeat Word'),
        ('repeat_sentence', 'Repeat Sentence'),
        ('describe_image', 'Describe Image'),
    ]
    
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='exercises')
    skill_area = models.ForeignKey(SkillArea, on_delete=models.CASCADE)
    exercise_type = models.CharField(max_length=50, choices=EXERCISE_TYPES)
    title = models.CharField(max_length=200)
    instruction = models.TextField()
    content = models.JSONField()  # Flexible JSON content based on exercise type
    correct_answer = models.JSONField()
    hints = models.JSONField(default=list)
    xp_reward = models.IntegerField(default=10)
    order = models.IntegerField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['lesson', 'order']
        unique_together = ['lesson', 'order']
    
    def __str__(self):
        return f"{self.title} - {self.lesson}"


class Game(models.Model):
    """
    Mini-games within lessons
    """
    GAME_TYPES = [
        ('memory_match', 'Memory Match'),
        ('sound_match', 'Sound Match'),
        ('sentence_race', 'Sentence Race'),
        ('vocabulary_hunt', 'Vocabulary Treasure Hunt'),
        ('grammar_puzzle', 'Grammar Puzzle'),
        ('listening_maze', 'Listening Maze'),
    ]
    
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='games')
    game_type = models.CharField(max_length=50, choices=GAME_TYPES)
    title = models.CharField(max_length=200)
    description = models.TextField()
    config = models.JSONField()  # Game-specific configuration
    xp_reward = models.IntegerField(default=50)
    order = models.IntegerField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['lesson', 'order']
    
    def __str__(self):
        return f"{self.title} - {self.lesson}"


class UserExerciseAttempt(models.Model):
    """
    Track user's exercise attempts for learning analytics
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='exercise_attempts')
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    answer = models.JSONField()
    score = models.IntegerField(default=0)  # 0-100
    max_score = models.IntegerField(default=100)
    completed = models.BooleanField(default=False)
    mistakes = models.JSONField(default=list)
    time_spent_seconds = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.exercise.title}"


class UserGameAttempt(models.Model):
    """
    Track user's game attempts
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='game_attempts')
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)
    time_spent_seconds = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.game.title}"
