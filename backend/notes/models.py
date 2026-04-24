from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Category(models.Model):
    """Note categories"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Note(models.Model):
    """Musical notes collection"""
    DIFFICULTY_LEVELS = [
        ('beginner', 'Boshlanuvchi'),
        ('intermediate', 'O\'rta'),
        ('advanced', 'Yuqori'),
        ('professional', 'Professional'),
    ]

    title = models.CharField(max_length=300)
    composer = models.CharField(max_length=200, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='notes')
    difficulty_level = models.CharField(max_length=20, choices=DIFFICULTY_LEVELS, default='beginner')
    description = models.TextField(blank=True)
    pdf_file = models.FileField(upload_to='notes/pdfs/', blank=True, null=True)
    audio_file = models.FileField(upload_to='notes/audio/', blank=True, null=True)
    image = models.ImageField(upload_to='notes/images/', blank=True, null=True)
    duration_minutes = models.PositiveIntegerField(blank=True, null=True)
    views_count = models.PositiveIntegerField(default=0)
    downloads_count = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class NoteRating(models.Model):
    """User ratings for notes"""
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # 1-5 stars
    review = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['note', 'user']

    def __str__(self):
        return f"{self.user.username} - {self.note.title} - {self.rating} stars"


class UserNoteProgress(models.Model):
    """Track user progress with notes"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='note_progress')
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='user_progress')
    is_completed = models.BooleanField(default=False)
    completion_percentage = models.IntegerField(default=0)  # 0-100
    practice_time_minutes = models.PositiveIntegerField(default=0)
    last_practiced = models.DateTimeField(blank=True, null=True)
    notes = models.TextField(blank=True)  # User's personal notes
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'note']

    def __str__(self):
        return f"{self.user.username} - {self.note.title} - {self.completion_percentage}%"


class PracticeSession(models.Model):
    """Track user practice sessions"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='practice_sessions')
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='practice_sessions', blank=True, null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(blank=True, null=True)
    duration_minutes = models.PositiveIntegerField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.duration_minutes} minutes"
