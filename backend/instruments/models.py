from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class InstrumentCategory(models.Model):
    """Instrument categories"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Instrument Categories"

    def __str__(self):
        return self.name


class Master(models.Model):
    """Instrument masters/craftsmen"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='master_profile')
    business_name = models.CharField(max_length=200)
    specialization = models.CharField(max_length=300)  # e.g., "Dutor, Tanbur"
    experience_years = models.PositiveIntegerField()
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)
    instagram = models.CharField(max_length=100, blank=True)
    telegram = models.CharField(max_length=100, blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    reviews_count = models.PositiveIntegerField(default=0)
    is_verified = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to='masters/avatars/', blank=True, null=True)
    banner_image = models.ImageField(upload_to='masters/banners/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.business_name}"


class MasterReview(models.Model):
    """Reviews for masters"""
    master = models.ForeignKey(Master, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # 1-5 stars
    review = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['master', 'user']

    def __str__(self):
        return f"{self.user.username} - {self.master.business_name} - {self.rating} stars"


class MasterWork(models.Model):
    """Portfolio of master's work"""
    master = models.ForeignKey(Master, on_delete=models.CASCADE, related_name='works')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='masters/works/')
    instrument_type = models.CharField(max_length=100)
    price_range = models.CharField(max_length=100, blank=True)  # e.g., "2-3 million so'm"
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.master.business_name} - {self.title}"


class InstrumentAccessory(models.Model):
    """Instrument accessories and parts"""
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.ForeignKey(InstrumentCategory, on_delete=models.CASCADE, related_name='accessories')
    price = models.DecimalField(max_digits=12, decimal_places=0)
    image = models.ImageField(upload_to='accessories/', blank=True, null=True)
    in_stock = models.BooleanField(default=True)
    master = models.ForeignKey(Master, on_delete=models.CASCADE, related_name='accessories', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class RepairService(models.Model):
    """Instrument repair services"""
    master = models.ForeignKey(Master, on_delete=models.CASCADE, related_name='repair_services')
    instrument_type = models.CharField(max_length=100)
    service_name = models.CharField(max_length=200)
    description = models.TextField()
    price_range = models.CharField(max_length=100)
    duration_days = models.PositiveIntegerField(help_text="Estimated duration in days")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.master.business_name} - {self.service_name}"


class Consultation(models.Model):
    """Consultation requests for masters"""
    master = models.ForeignKey(Master, on_delete=models.CASCADE, related_name='consultations')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    message = models.TextField()
    consultation_type = models.CharField(
        max_length=20,
        choices=[
            ('purchase', 'Xarid maslahati'),
            ('repair', 'Ta\'mir maslahati'),
            ('learning', 'O\'rganish maslahati'),
            ('other', 'Boshqa'),
        ],
        default='other'
    )
    is_contacted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.master.business_name}"
