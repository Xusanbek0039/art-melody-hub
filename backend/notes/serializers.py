from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Category, Note, NoteRating, UserNoteProgress, PracticeSession

User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    notes_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'icon', 'notes_count', 'created_at']

    def get_notes_count(self, obj):
        return obj.notes.count()


class NoteSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)
    average_rating = serializers.SerializerMethodField()
    ratings_count = serializers.SerializerMethodField()
    is_rated_by_user = serializers.SerializerMethodField()
    user_progress = serializers.SerializerMethodField()

    class Meta:
        model = Note
        fields = ['id', 'title', 'composer', 'category', 'category_id', 'difficulty_level',
                 'description', 'pdf_file', 'audio_file', 'image', 'duration_minutes',
                 'views_count', 'downloads_count', 'is_featured', 'average_rating',
                 'ratings_count', 'is_rated_by_user', 'user_progress', 'created_at', 'updated_at']
        read_only_fields = ['views_count', 'downloads_count', 'created_at', 'updated_at']

    def get_average_rating(self, obj):
        ratings = obj.ratings.all()
        if ratings:
            return sum(rating.rating for rating in ratings) / len(ratings)
        return 0

    def get_ratings_count(self, obj):
        return obj.ratings.count()

    def get_is_rated_by_user(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.ratings.filter(user=request.user).exists()
        return False

    def get_user_progress(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            try:
                progress = obj.user_progress.get(user=request.user)
                return {
                    'is_completed': progress.is_completed,
                    'completion_percentage': progress.completion_percentage,
                    'practice_time_minutes': progress.practice_time_minutes,
                    'last_practiced': progress.last_practiced,
                    'notes': progress.notes
                }
            except UserNoteProgress.DoesNotExist:
                return None
        return None


class NoteRatingSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    note = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = NoteRating
        fields = ['id', 'note', 'user', 'rating', 'review', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5")
        return value


class UserNoteProgressSerializer(serializers.ModelSerializer):
    note = NoteSerializer(read_only=True)
    note_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = UserNoteProgress
        fields = ['id', 'note', 'note_id', 'is_completed', 'completion_percentage',
                 'practice_time_minutes', 'last_practiced', 'notes', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_completion_percentage(self, value):
        if value < 0 or value > 100:
            raise serializers.ValidationError("Completion percentage must be between 0 and 100")
        return value


class PracticeSessionSerializer(serializers.ModelSerializer):
    note = NoteSerializer(read_only=True)
    note_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = PracticeSession
        fields = ['id', 'note', 'note_id', 'user', 'start_time', 'end_time',
                 'duration_minutes', 'notes', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']


class SimpleNoteSerializer(serializers.ModelSerializer):
    """Simplified serializer for lists"""
    category = CategorySerializer(read_only=True)
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Note
        fields = ['id', 'title', 'composer', 'category', 'difficulty_level',
                 'image', 'duration_minutes', 'average_rating', 'is_featured', 'created_at']

    def get_average_rating(self, obj):
        ratings = obj.ratings.all()
        if ratings:
            return sum(rating.rating for rating in ratings) / len(ratings)
        return 0
