from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class UserActivity(models.Model):
    """Track user activities for analytics"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=50)  # login, note_view, test_taken, etc.
    activity_data = models.JSONField(default=dict, blank=True)  # Additional data
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user', 'timestamp']),
            models.Index(fields=['activity_type', 'timestamp']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.activity_type} - {self.timestamp}"


class DailyStats(models.Model):
    """Daily aggregated statistics"""
    date = models.DateField(unique=True)
    total_users = models.PositiveIntegerField(default=0)
    active_users = models.PositiveIntegerField(default=0)
    new_users = models.PositiveIntegerField(default=0)
    total_sessions = models.PositiveIntegerField(default=0)
    total_practice_time_minutes = models.PositiveIntegerField(default=0)
    notes_downloaded = models.PositiveIntegerField(default=0)
    tests_completed = models.PositiveIntegerField(default=0)
    orders_placed = models.PositiveIntegerField(default=0)
    revenue = models.DecimalField(max_digits=12, decimal_places=0, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"Stats for {self.date}"


class PopularContent(models.Model):
    """Track popular content"""
    CONTENT_TYPES = [
        ('note', 'Note'),
        ('product', 'Product'),
        ('test', 'Test'),
        ('topic', 'Theory Topic'),
        ('master', 'Master'),
    ]

    content_type = models.CharField(max_length=20, choices=CONTENT_TYPES)
    content_id = models.PositiveIntegerField()
    views_count = models.PositiveIntegerField(default=0)
    likes_count = models.PositiveIntegerField(default=0)
    downloads_count = models.PositiveIntegerField(default=0)
    shares_count = models.PositiveIntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['content_type', 'content_id']
        indexes = [
            models.Index(fields=['content_type', 'views_count']),
            models.Index(fields=['content_type', 'likes_count']),
        ]

    def __str__(self):
        return f"{self.get_content_type_display()} {self.content_id} - {self.views_count} views"


class UserEngagement(models.Model):
    """Track user engagement metrics"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='engagement')
    total_sessions = models.PositiveIntegerField(default=0)
    total_practice_time_minutes = models.PositiveIntegerField(default=0)
    total_notes_viewed = models.PositiveIntegerField(default=0)
    total_notes_downloaded = models.PositiveIntegerField(default=0)
    total_tests_taken = models.PositiveIntegerField(default=0)
    total_tests_passed = models.PositiveIntegerField(default=0)
    total_orders_placed = models.PositiveIntegerField(default=0)
    total_spent = models.DecimalField(max_digits=12, decimal_places=0, default=0)
    last_login = models.DateTimeField(blank=True, null=True)
    streak_days = models.PositiveIntegerField(default=0)  # Consecutive days active
    longest_streak = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} Engagement"

    @property
    def average_session_duration(self):
        if self.total_sessions == 0:
            return 0
        return self.total_practice_time_minutes / self.total_sessions

    @property
    def test_pass_rate(self):
        if self.total_tests_taken == 0:
            return 0
        return (self.total_tests_passed / self.total_tests_taken) * 100


class LearningPath(models.Model):
    """User learning paths and recommendations"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='learning_paths')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    difficulty_level = models.CharField(max_length=20, choices=[
        ('beginner', 'Boshlanuvchi'),
        ('intermediate', 'O\'rta'),
        ('advanced', 'Yuqori'),
        ('professional', 'Professional'),
    ])
    estimated_hours = models.PositiveIntegerField(default=0)
    completion_percentage = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.title}"


class LearningPathItem(models.Model):
    """Individual items in a learning path"""
    ITEM_TYPES = [
        ('note', 'Note'),
        ('theory_topic', 'Theory Topic'),
        ('test', 'Test'),
        ('practice_session', 'Practice Session'),
        ('video', 'Video'),
    ]

    learning_path = models.ForeignKey(LearningPath, on_delete=models.CASCADE, related_name='items')
    item_type = models.CharField(max_length=20, choices=ITEM_TYPES)
    item_id = models.PositiveIntegerField()
    title = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    is_completed = models.BooleanField(default=False)
    completion_date = models.DateTimeField(blank=True, null=True)
    estimated_minutes = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        unique_together = ['learning_path', 'item_type', 'item_id']

    def __str__(self):
        return f"{self.learning_path.title} - {self.title}"


class PerformanceMetric(models.Model):
    """Track various performance metrics"""
    metric_name = models.CharField(max_length=100)
    metric_value = models.DecimalField(max_digits=15, decimal_places=2)
    metric_unit = models.CharField(max_length=20, blank=True)  # percentage, count, minutes, etc.
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['metric_name', 'date']
        ordering = ['-date']

    def __str__(self):
        return f"{self.metric_name}: {self.metric_value} {self.metric_unit} on {self.date}"
