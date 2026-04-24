from django.contrib import admin
from .models import (
    UserActivity, DailyStats, PopularContent, UserEngagement,
    LearningPath, LearningPathItem, PerformanceMetric
)


@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    list_display = ['user', 'activity_type', 'timestamp', 'ip_address']
    list_filter = ['activity_type', 'timestamp']
    search_fields = ['user__username', 'activity_type']
    ordering = ['-timestamp']
    readonly_fields = ['timestamp']
    
    fieldsets = (
        ('Activity Info', {
            'fields': ('user', 'activity_type', 'activity_data')
        }),
        ('Request Info', {
            'fields': ('ip_address', 'user_agent')
        }),
        ('Timestamp', {
            'fields': ('timestamp',)
        }),
    )


@admin.register(DailyStats)
class DailyStatsAdmin(admin.ModelAdmin):
    list_display = ['date', 'total_users', 'active_users', 'new_users', 'total_sessions', 'revenue']
    list_filter = ['date']
    ordering = ['-date']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('User Stats', {
            'fields': ('total_users', 'active_users', 'new_users')
        }),
        ('Activity Stats', {
            'fields': ('total_sessions', 'total_practice_time_minutes', 'notes_downloaded', 'tests_completed')
        }),
        ('Commerce Stats', {
            'fields': ('orders_placed', 'revenue')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(PopularContent)
class PopularContentAdmin(admin.ModelAdmin):
    list_display = ['content_type', 'content_id', 'views_count', 'likes_count', 'downloads_count', 'last_updated']
    list_filter = ['content_type', 'last_updated']
    ordering = ['-views_count']
    readonly_fields = ['last_updated']


class LearningPathItemInline(admin.TabularInline):
    model = LearningPathItem
    extra = 3
    fields = ['item_type', 'item_id', 'title', 'order', 'is_completed', 'estimated_minutes']


@admin.register(LearningPath)
class LearningPathAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'difficulty_level', 'completion_percentage', 'is_completed', 'created_at']
    list_filter = ['difficulty_level', 'is_completed', 'created_at']
    search_fields = ['user__username', 'title', 'description']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [LearningPathItemInline]


@admin.register(LearningPathItem)
class LearningPathItemAdmin(admin.ModelAdmin):
    list_display = ['learning_path', 'item_type', 'title', 'order', 'is_completed', 'estimated_minutes']
    list_filter = ['item_type', 'is_completed']
    search_fields = ['learning_path__title', 'title', 'description']
    ordering = ['learning_path', 'order']


@admin.register(UserEngagement)
class UserEngagementAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_sessions', 'total_practice_time_minutes', 'total_tests_taken',
                   'total_orders_placed', 'streak_days', 'last_login']
    list_filter = ['last_login', 'created_at']
    search_fields = ['user__username']
    ordering = ['-last_login']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(PerformanceMetric)
class PerformanceMetricAdmin(admin.ModelAdmin):
    list_display = ['metric_name', 'metric_value', 'metric_unit', 'date']
    list_filter = ['metric_name', 'date']
    ordering = ['-date']
    readonly_fields = ['created_at']
