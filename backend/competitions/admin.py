from django.contrib import admin
from .models import (
    Competition, CompetitionCategory, Registration, Result,
    Judge, Schedule, News
)


@admin.register(Competition)
class CompetitionAdmin(admin.ModelAdmin):
    list_display = ['title', 'level', 'status', 'location', 'start_date', 'registration_end', 'is_featured']
    list_filter = ['level', 'status', 'is_featured', 'start_date']
    search_fields = ['title', 'organizer', 'location']
    ordering = ['start_date']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('title', 'description', 'level', 'status', 'organizer', 'is_featured')
        }),
        ('Dates', {
            'fields': ('start_date', 'end_date', 'registration_start', 'registration_end')
        }),
        ('Location & Contact', {
            'fields': ('location', 'contact_phone', 'contact_email', 'website')
        }),
        ('Requirements', {
            'fields': ('age_requirements', 'instrument_requirements', 'application_fee', 'prize_fund')
        }),
        ('Files', {
            'fields': ('poster_image', 'regulations_file')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(CompetitionCategory)
class CompetitionCategoryAdmin(admin.ModelAdmin):
    list_display = ['competition', 'name', 'age_group', 'registration_fee', 'max_participants']
    list_filter = ['age_group', 'registration_fee']
    search_fields = ['competition__title', 'name', 'description']
    ordering = ['competition', 'name']


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ['user', 'competition', 'category', 'status', 'piece_title', 'payment_status', 'created_at']
    list_filter = ['status', 'payment_status', 'created_at']
    search_fields = ['user__username', 'competition__title', 'piece_title', 'composer']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('user', 'competition', 'category', 'status')
        }),
        ('Performance Details', {
            'fields': ('piece_title', 'composer', 'duration_minutes')
        }),
        ('Personal Info', {
            'fields': ('teacher_name', 'teacher_phone', 'institution', 'experience_years')
        }),
        ('Additional Info', {
            'fields': ('previous_achievements', 'special_needs', 'notes')
        }),
        ('Payment', {
            'fields': ('payment_status', 'payment_reference')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ['registration', 'position', 'points', 'prize_awarded', 'announced_at']
    list_filter = ['position', 'announced_at']
    search_fields = ['registration__user__username', 'registration__competition__title']
    ordering = ['-announced_at']
    readonly_fields = ['announced_at']


@admin.register(Judge)
class JudgeAdmin(admin.ModelAdmin):
    list_display = ['name', 'competition', 'position', 'institution', 'is_chairman', 'order']
    list_filter = ['is_chairman', 'competition']
    search_fields = ['name', 'competition__title', 'institution']
    ordering = ['competition', 'order']


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ['competition', 'date', 'time', 'event_title', 'location', 'duration_minutes']
    list_filter = ['date', 'competition']
    search_fields = ['competition__title', 'event_title', 'location']
    ordering = ['date', 'time']
    date_hierarchy = 'date'


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['competition', 'title', 'is_announcement', 'created_at']
    list_filter = ['is_announcement', 'created_at']
    search_fields = ['competition__title', 'title', 'content']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']
