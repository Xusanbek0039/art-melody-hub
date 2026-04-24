from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Profile, Achievement, CompetitionParticipation


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'phone', 'region', 'is_master', 'created_at']
    list_filter = ['is_master', 'is_staff', 'is_active', 'region', 'created_at']
    search_fields = ['username', 'email', 'first_name', 'last_name', 'phone']
    ordering = ['-created_at']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('phone', 'region', 'address', 'bio', 'avatar', 'specialization', 'education', 'is_master')
        }),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Additional Info', {
            'fields': ('email', 'phone', 'region', 'specialization')
        }),
    )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'practice_time_hours', 'competitions_count', 'achievements_count', 'skill_level']
    list_filter = ['skill_level']
    search_fields = ['user__username', 'user__first_name', 'user__last_name']


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'earned_at']
    list_filter = ['earned_at']
    search_fields = ['user__username', 'title']
    date_hierarchy = 'earned_at'


@admin.register(CompetitionParticipation)
class CompetitionParticipationAdmin(admin.ModelAdmin):
    list_display = ['user', 'competition_name', 'year', 'result', 'is_winner']
    list_filter = ['year', 'is_winner']
    search_fields = ['user__username', 'competition_name', 'result']
