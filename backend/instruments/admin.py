from django.contrib import admin
from .models import (
    InstrumentCategory, Master, MasterReview, MasterWork,
    InstrumentAccessory, RepairService, Consultation
)


@admin.register(InstrumentCategory)
class InstrumentCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['name']


@admin.register(Master)
class MasterAdmin(admin.ModelAdmin):
    list_display = ['user', 'business_name', 'specialization', 'location', 
                   'experience_years', 'rating', 'reviews_count', 'is_verified', 'created_at']
    list_filter = ['is_verified', 'experience_years', 'created_at']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 
                     'business_name', 'specialization', 'location']
    ordering = ['-created_at']
    readonly_fields = ['rating', 'reviews_count', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('user', 'business_name', 'specialization', 'experience_years', 'bio')
        }),
        ('Contact Info', {
            'fields': ('location', 'phone', 'email', 'website', 'instagram', 'telegram')
        }),
        ('Media', {
            'fields': ('avatar', 'banner_image')
        }),
        ('Statistics', {
            'fields': ('rating', 'reviews_count', 'is_verified')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(MasterReview)
class MasterReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'master', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['user__username', 'master__business_name', 'review']
    ordering = ['-created_at']


@admin.register(MasterWork)
class MasterWorkAdmin(admin.ModelAdmin):
    list_display = ['master', 'title', 'instrument_type', 'price_range', 'is_featured', 'created_at']
    list_filter = ['is_featured', 'instrument_type', 'created_at']
    search_fields = ['master__business_name', 'title', 'description']
    ordering = ['-created_at']


@admin.register(InstrumentAccessory)
class InstrumentAccessoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'in_stock', 'master', 'created_at']
    list_filter = ['in_stock', 'category', 'created_at']
    search_fields = ['name', 'description', 'master__business_name']
    ordering = ['-created_at']


@admin.register(RepairService)
class RepairServiceAdmin(admin.ModelAdmin):
    list_display = ['master', 'instrument_type', 'service_name', 'price_range', 'duration_days', 'created_at']
    list_filter = ['instrument_type', 'duration_days', 'created_at']
    search_fields = ['master__business_name', 'service_name', 'description']
    ordering = ['-created_at']


@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):
    list_display = ['name', 'master', 'consultation_type', 'phone', 'is_contacted', 'created_at']
    list_filter = ['consultation_type', 'is_contacted', 'created_at']
    search_fields = ['name', 'phone', 'email', 'message']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'
