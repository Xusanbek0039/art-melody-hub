from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class TheoryLevel(models.Model):
    """Music theory difficulty levels"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name


class TheoryTopic(models.Model):
    """Music theory topics"""
    name = models.CharField(max_length=200)
    description = models.TextField()
    level = models.ForeignKey(TheoryLevel, on_delete=models.CASCADE, related_name='topics')
    content = models.TextField(blank=True)  # Main theory content
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['level', 'order']

    def __str__(self):
        return f"{self.level.name} - {self.name}"


class TheoryTest(models.Model):
    """Music theory tests"""
    title = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    level = models.ForeignKey(TheoryLevel, on_delete=models.CASCADE, related_name='tests')
    topic = models.ForeignKey(TheoryTopic, on_delete=models.CASCADE, related_name='tests', blank=True, null=True)
    time_limit_minutes = models.PositiveIntegerField(default=30)
    passing_score = models.IntegerField(default=70)  # Percentage
    max_attempts = models.PositiveIntegerField(default=3)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.level.name})"


class Question(models.Model):
    """Test questions"""
    QUESTION_TYPES = [
        ('multiple_choice', 'Multiple Choice'),
        ('true_false', 'True/False'),
        ('fill_blank', 'Fill in the Blank'),
        ('matching', 'Matching'),
        ('audio', 'Audio Recognition'),
    ]

    test = models.ForeignKey(TheoryTest, on_delete=models.CASCADE, related_name='questions')
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES)
    question_text = models.TextField()
    explanation = models.TextField(blank=True)  # Explanation for correct answer
    order = models.PositiveIntegerField(default=0)
    points = models.IntegerField(default=1)
    audio_file = models.FileField(upload_to='theory/audio/', blank=True, null=True)
    image = models.ImageField(upload_to='theory/images/', blank=True, null=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Question {self.order + 1} - {self.test.title}"


class Choice(models.Model):
    """Multiple choice options"""
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    choice_text = models.CharField(max_length=500)
    is_correct = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Choice {self.order + 1} - {self.choice_text}"


class TestAttempt(models.Model):
    """User test attempts"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='test_attempts')
    test = models.ForeignKey(TheoryTest, on_delete=models.CASCADE, related_name='attempts')
    score = models.IntegerField()  # Percentage
    total_points = models.IntegerField()
    earned_points = models.IntegerField()
    started_at = models.DateTimeField()
    completed_at = models.DateTimeField(blank=True, null=True)
    time_taken_minutes = models.PositiveIntegerField(blank=True, null=True)
    is_passed = models.BooleanField(default=False)
    attempt_number = models.PositiveIntegerField()

    class Meta:
        unique_together = ['user', 'test', 'attempt_number']
        ordering = ['-started_at']

    def __str__(self):
        return f"{self.user.username} - {self.test.title} - {self.score}%"


class Answer(models.Model):
    """User answers to questions"""
    attempt = models.ForeignKey(TestAttempt, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_choice = models.ForeignKey(Choice, on_delete=models.CASCADE, blank=True, null=True)
    text_answer = models.TextField(blank=True)  # For fill-in-the-blank questions
    is_correct = models.BooleanField(default=False)
    points_earned = models.IntegerField(default=0)

    class Meta:
        unique_together = ['attempt', 'question']

    def __str__(self):
        return f"Answer to {self.question.question_text[:50]}..."


class TheoryResource(models.Model):
    """Additional learning resources"""
    RESOURCE_TYPES = [
        ('video', 'Video'),
        ('document', 'Document'),
        ('audio', 'Audio'),
        ('image', 'Image'),
        ('link', 'External Link'),
    ]

    title = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    resource_type = models.CharField(max_length=20, choices=RESOURCE_TYPES)
    topic = models.ForeignKey(TheoryTopic, on_delete=models.CASCADE, related_name='resources', blank=True, null=True)
    file = models.FileField(upload_to='theory/resources/', blank=True, null=True)
    url = models.URLField(blank=True)
    duration_minutes = models.PositiveIntegerField(blank=True, null=True)
    is_free = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class UserProgress(models.Model):
    """Track user progress in theory topics"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='theory_progress')
    topic = models.ForeignKey(TheoryTopic, on_delete=models.CASCADE, related_name='user_progress')
    is_completed = models.BooleanField(default=False)
    completion_percentage = models.IntegerField(default=0)  # 0-100
    time_spent_minutes = models.PositiveIntegerField(default=0)
    last_accessed = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'topic']

    def __str__(self):
        return f"{self.user.username} - {self.topic.name} - {self.completion_percentage}%"


class StudySession(models.Model):
    """User study sessions"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='study_sessions')
    topic = models.ForeignKey(TheoryTopic, on_delete=models.CASCADE, related_name='study_sessions', blank=True, null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(blank=True, null=True)
    duration_minutes = models.PositiveIntegerField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.duration_minutes} minutes"
