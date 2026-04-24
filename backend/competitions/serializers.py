from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import (
    Competition, CompetitionCategory, Registration, Result,
    Judge, Schedule, News
)

User = get_user_model()


class CompetitionCategorySerializer(serializers.ModelSerializer):
    registrations_count = serializers.SerializerMethodField()

    class Meta:
        model = CompetitionCategory
        fields = ['id', 'name', 'description', 'age_group', 'max_participants',
                 'registration_fee', 'prize_1', 'prize_2', 'prize_3', 'registrations_count']

    def get_registrations_count(self, obj):
        return obj.registrations.count()


class CompetitionSerializer(serializers.ModelSerializer):
    categories = CompetitionCategorySerializer(many=True, read_only=True)
    registrations_count = serializers.SerializerMethodField()
    is_registration_open = serializers.BooleanField(read_only=True)
    days_until_registration = serializers.IntegerField(read_only=True)

    class Meta:
        model = Competition
        fields = ['id', 'title', 'description', 'level', 'status', 'organizer',
                 'location', 'start_date', 'end_date', 'registration_start',
                 'registration_end', 'age_requirements', 'instrument_requirements',
                 'prize_fund', 'application_fee', 'contact_phone', 'contact_email',
                 'website', 'poster_image', 'regulations_file', 'is_featured',
                 'categories', 'registrations_count', 'is_registration_open',
                 'days_until_registration', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class SimpleCompetitionSerializer(serializers.ModelSerializer):
    """Simplified serializer for lists"""
    categories_count = serializers.SerializerMethodField()

    class Meta:
        model = Competition
        fields = ['id', 'title', 'level', 'status', 'location', 'start_date',
                 'registration_end', 'poster_image', 'is_featured', 'categories_count']

    def get_categories_count(self, obj):
        return obj.categories.count()


class RegistrationSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    competition = CompetitionSerializer(read_only=True)
    competition_id = serializers.IntegerField(write_only=True)
    category = CompetitionCategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Registration
        fields = ['id', 'user', 'competition', 'competition_id', 'category', 'category_id',
                 'status', 'piece_title', 'composer', 'duration_minutes', 'teacher_name',
                 'teacher_phone', 'institution', 'experience_years', 'previous_achievements',
                 'special_needs', 'payment_status', 'payment_reference', 'notes',
                 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']


class ResultSerializer(serializers.ModelSerializer):
    registration = RegistrationSerializer(read_only=True)
    registration_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Result
        fields = ['id', 'registration', 'registration_id', 'position', 'points',
                 'certificate_url', 'prize_awarded', 'judge_comments', 'announced_at']
        read_only_fields = ['id', 'announced_at']


class JudgeSerializer(serializers.ModelSerializer):
    competition = CompetitionSerializer(read_only=True)
    competition_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Judge
        fields = ['id', 'competition', 'competition_id', 'name', 'position', 'institution',
                 'bio', 'photo', 'is_chairman', 'order']

    def validate_order(self, value):
        if value < 0:
            raise serializers.ValidationError("Order must be non-negative")
        return value


class ScheduleSerializer(serializers.ModelSerializer):
    competition = CompetitionSerializer(read_only=True)
    competition_id = serializers.IntegerField(write_only=True)
    category = CompetitionCategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = Schedule
        fields = ['id', 'competition', 'competition_id', 'date', 'time', 'category',
                 'category_id', 'event_title', 'description', 'location', 'duration_minutes']


class NewsSerializer(serializers.ModelSerializer):
    competition = CompetitionSerializer(read_only=True)
    competition_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = News
        fields = ['id', 'competition', 'competition_id', 'title', 'content', 'image',
                 'is_announcement', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user's own registrations"""
    competition = SimpleCompetitionSerializer(read_only=True)
    category = CompetitionCategorySerializer(read_only=True)
    result = ResultSerializer(read_only=True)

    class Meta:
        model = Registration
        fields = ['id', 'competition', 'category', 'status', 'piece_title', 'composer',
                 'duration_minutes', 'teacher_name', 'teacher_phone', 'institution',
                 'experience_years', 'previous_achievements', 'payment_status',
                 'payment_reference', 'notes', 'result', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
