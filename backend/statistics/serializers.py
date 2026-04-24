from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import (
    UserActivity, DailyStats, PopularContent, UserEngagement,
    LearningPath, LearningPathItem, PerformanceMetric
)

User = get_user_model()


class UserActivitySerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = UserActivity
        fields = ['id', 'user', 'activity_type', 'activity_data', 'ip_address',
                 'user_agent', 'timestamp']
        read_only_fields = ['id', 'timestamp']


class DailyStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyStats
        fields = ['id', 'date', 'total_users', 'active_users', 'new_users',
                 'total_sessions', 'total_practice_time_minutes', 'notes_downloaded',
                 'tests_completed', 'orders_placed', 'revenue', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class PopularContentSerializer(serializers.ModelSerializer):
    content_type_display = serializers.CharField(source='get_content_type_display', read_only=True)

    class Meta:
        model = PopularContent
        fields = ['id', 'content_type', 'content_type_display', 'content_id',
                 'views_count', 'likes_count', 'downloads_count', 'shares_count', 'last_updated']
        read_only_fields = ['id', 'last_updated']


class UserEngagementSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    average_session_duration = serializers.FloatField(read_only=True)
    test_pass_rate = serializers.FloatField(read_only=True)

    class Meta:
        model = UserEngagement
        fields = ['id', 'user', 'total_sessions', 'total_practice_time_minutes',
                 'total_notes_viewed', 'total_notes_downloaded', 'total_tests_taken',
                 'total_tests_passed', 'total_orders_placed', 'total_spent',
                 'last_login', 'streak_days', 'longest_streak',
                 'average_session_duration', 'test_pass_rate', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class LearningPathItemSerializer(serializers.ModelSerializer):
    item_type_display = serializers.CharField(source='get_item_type_display', read_only=True)

    class Meta:
        model = LearningPathItem
        fields = ['id', 'item_type', 'item_type_display', 'item_id', 'title',
                 'description', 'order', 'is_completed', 'completion_date', 'estimated_minutes']
        read_only_fields = ['id', 'completion_date']


class LearningPathSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    items = LearningPathItemSerializer(many=True, read_only=True)
    difficulty_level_display = serializers.CharField(source='get_difficulty_level_display', read_only=True)

    class Meta:
        model = LearningPath
        fields = ['id', 'user', 'title', 'description', 'difficulty_level',
                 'difficulty_level_display', 'estimated_hours', 'completion_percentage',
                 'is_active', 'is_completed', 'items', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class PerformanceMetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerformanceMetric
        fields = ['id', 'metric_name', 'metric_value', 'metric_unit', 'date', 'created_at']
        read_only_fields = ['id', 'created_at']


class DashboardStatsSerializer(serializers.Serializer):
    """Serializer for dashboard statistics"""
    total_users = serializers.IntegerField()
    active_users_today = serializers.IntegerField()
    new_users_today = serializers.IntegerField()
    total_sessions_today = serializers.IntegerField()
    total_practice_time_today = serializers.IntegerField()
    notes_downloaded_today = serializers.IntegerField()
    tests_completed_today = serializers.IntegerField()
    orders_placed_today = serializers.IntegerField()
    revenue_today = serializers.DecimalField(max_digits=12, decimal_places=2)
    popular_notes = serializers.ListField()
    popular_products = serializers.ListField()
    user_growth = serializers.ListField()
    revenue_trend = serializers.ListField()


class UserStatsSerializer(serializers.Serializer):
    """Serializer for individual user statistics"""
    total_practice_time = serializers.IntegerField()
    total_sessions = serializers.IntegerField()
    notes_viewed = serializers.IntegerField()
    notes_downloaded = serializers.IntegerField()
    tests_taken = serializers.IntegerField()
    tests_passed = serializers.IntegerField()
    test_pass_rate = serializers.FloatField()
    orders_placed = serializers.IntegerField()
    total_spent = serializers.DecimalField(max_digits=12, decimal_places=2)
    streak_days = serializers.IntegerField()
    average_session_duration = serializers.FloatField()
    recent_activities = serializers.ListField()
    learning_progress = serializers.DictField()
    achievements = serializers.ListField()


class ContentAnalyticsSerializer(serializers.Serializer):
    """Serializer for content analytics"""
    total_views = serializers.IntegerField()
    total_likes = serializers.IntegerField()
    total_downloads = serializers.IntegerField()
    engagement_rate = serializers.FloatField()
    top_performing_content = serializers.ListField()
    views_by_category = serializers.DictField()
    views_by_date = serializers.ListField()
    user_demographics = serializers.DictField()


class LearningAnalyticsSerializer(serializers.Serializer):
    """Serializer for learning analytics"""
    total_learning_time = serializers.IntegerField()
    average_session_duration = serializers.FloatField()
    completion_rates = serializers.DictField()
    popular_topics = serializers.ListField()
    difficulty_distribution = serializers.DictField()
    learning_paths_created = serializers.IntegerField()
    learning_paths_completed = serializers.IntegerField()
