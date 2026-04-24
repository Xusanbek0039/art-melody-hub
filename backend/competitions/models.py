from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Competition(models.Model):
    """Music competitions"""
    STATUS_CHOICES = [
        ('upcoming', 'Kelayotgan'),
        ('registration', 'Ro\'yxatga olish'),
        ('active', 'Faol'),
        ('completed', 'Tugallangan'),
        ('cancelled', 'Bekor qilingan'),
    ]

    LEVEL_CHOICES = [
        ('local', 'Mahalliy'),
        ('regional', 'Viloyat'),
        ('national', 'Respublika'),
        ('international', 'Xalqaro'),
    ]

    title = models.CharField(max_length=300)
    description = models.TextField()
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='upcoming')
    organizer = models.CharField(max_length=200)
    location = models.CharField(max_length=300)
    start_date = models.DateField()
    end_date = models.DateField()
    registration_start = models.DateField()
    registration_end = models.DateField()
    age_requirements = models.CharField(max_length=100, blank=True)
    instrument_requirements = models.TextField(blank=True)
    prize_fund = models.CharField(max_length=200, blank=True)
    application_fee = models.DecimalField(max_digits=12, decimal_places=0, default=0)
    contact_phone = models.CharField(max_length=20)
    contact_email = models.EmailField(blank=True)
    website = models.URLField(blank=True)
    poster_image = models.ImageField(upload_to='competitions/posters/', blank=True, null=True)
    regulations_file = models.FileField(upload_to='competitions/regulations/', blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.start_date.year})"

    @property
    def is_registration_open(self):
        from django.utils import timezone
        today = timezone.now().date()
        return self.registration_start <= today <= self.registration_end

    @property
    def days_until_registration(self):
        from django.utils import timezone
        today = timezone.now().date()
        if today < self.registration_start:
            return (self.registration_start - today).days
        return 0


class CompetitionCategory(models.Model):
    """Competition categories (e.g., tanbur, dutor, vocal)"""
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, related_name='categories')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    age_group = models.CharField(max_length=50, blank=True)  # e.g., "14-18 years"
    max_participants = models.PositiveIntegerField(blank=True, null=True)
    registration_fee = models.DecimalField(max_digits=12, decimal_places=0, default=0)
    prize_1 = models.CharField(max_length=200, blank=True)
    prize_2 = models.CharField(max_length=200, blank=True)
    prize_3 = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.competition.title} - {self.name}"


class Registration(models.Model):
    """Competition registrations"""
    STATUS_CHOICES = [
        ('pending', 'Kutilmoqda'),
        ('approved', 'Tasdiqlangan'),
        ('rejected', 'Rad etilgan'),
        ('withdrawn', 'Chekinilgan'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='competition_registrations')
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, related_name='registrations')
    category = models.ForeignKey(CompetitionCategory, on_delete=models.CASCADE, related_name='registrations')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    piece_title = models.CharField(max_length=300)
    composer = models.CharField(max_length=200, blank=True)
    duration_minutes = models.PositiveIntegerField()
    teacher_name = models.CharField(max_length=200, blank=True)
    teacher_phone = models.CharField(max_length=20, blank=True)
    institution = models.CharField(max_length=300, blank=True)
    experience_years = models.PositiveIntegerField(blank=True, null=True)
    previous_achievements = models.TextField(blank=True)
    special_needs = models.TextField(blank=True)
    payment_status = models.BooleanField(default=False)
    payment_reference = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'competition', 'category']

    def __str__(self):
        return f"{self.user.username} - {self.competition.title}"


class Result(models.Model):
    """Competition results"""
    registration = models.OneToOneField(Registration, on_delete=models.CASCADE, related_name='result')
    position = models.PositiveIntegerField(blank=True, null=True)  # 1, 2, 3, etc.
    points = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    certificate_url = models.URLField(blank=True)
    prize_awarded = models.CharField(max_length=200, blank=True)
    judge_comments = models.TextField(blank=True)
    announced_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.registration.user.username} - {self.registration.competition.title} - {self.position}"


class Judge(models.Model):
    """Competition judges"""
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, related_name='judges')
    name = models.CharField(max_length=200)
    position = models.CharField(max_length=200)
    institution = models.CharField(max_length=300)
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to='judges/', blank=True, null=True)
    is_chairman = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.name} - {self.competition.title}"


class Schedule(models.Model):
    """Competition schedule"""
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, related_name='schedule')
    date = models.DateField()
    time = models.TimeField()
    category = models.ForeignKey(CompetitionCategory, on_delete=models.CASCADE, blank=True, null=True)
    event_title = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=300)
    duration_minutes = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.competition.title} - {self.event_title} ({self.date})"


class News(models.Model):
    """Competition news and updates"""
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, related_name='news')
    title = models.CharField(max_length=300)
    content = models.TextField()
    image = models.ImageField(upload_to='competitions/news/', blank=True, null=True)
    is_announcement = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.competition.title} - {self.title}"
