from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom user model for Art Melody Hub"""
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True, unique=True)
    region = models.CharField(max_length=100, blank=True)
    address = models.TextField(blank=True)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    specialization = models.CharField(max_length=200, blank=True)
    education = models.CharField(max_length=300, blank=True)
    is_master = models.BooleanField(default=False)  # For instrument masters
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name}" if self.first_name else self.username


class Profile(models.Model):
    """Extended profile information"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    practice_time_hours = models.PositiveIntegerField(default=0)
    competitions_count = models.PositiveIntegerField(default=0)
    achievements_count = models.PositiveIntegerField(default=0)
    preferred_instrument = models.CharField(max_length=100, blank=True)
    skill_level = models.CharField(
        max_length=20,
        choices=[
            ('beginner', 'Boshlanuvchi'),
            ('intermediate', 'O\'rta'),
            ('advanced', 'Yuqori'),
            ('professional', 'Professional'),
        ],
        default='beginner'
    )

    def __str__(self):
        return f"{self.user.username} Profile"


class Achievement(models.Model):
    """User achievements"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='achievements')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)  # Icon class name
    earned_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.title}"


class CompetitionParticipation(models.Model):
    """User's competition participation history"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='competition_participations')
    competition_name = models.CharField(max_length=300)
    year = models.PositiveIntegerField()
    result = models.CharField(max_length=200)
    is_winner = models.BooleanField(default=False)
    certificate_url = models.URLField(blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.competition_name} ({self.year})"
