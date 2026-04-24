from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import (
    TheoryLevel, TheoryTopic, TheoryTest, Question, Choice,
    TestAttempt, Answer, TheoryResource, UserProgress, StudySession
)

User = get_user_model()


class TheoryLevelSerializer(serializers.ModelSerializer):
    topics_count = serializers.SerializerMethodField()
    tests_count = serializers.SerializerMethodField()

    class Meta:
        model = TheoryLevel
        fields = ['id', 'name', 'description', 'order', 'is_active', 'topics_count', 'tests_count', 'created_at']

    def get_topics_count(self, obj):
        return obj.topics.filter(is_active=True).count()

    def get_tests_count(self, obj):
        return obj.tests.filter(is_active=True).count()


class TheoryTopicSerializer(serializers.ModelSerializer):
    level = TheoryLevelSerializer(read_only=True)
    level_id = serializers.IntegerField(write_only=True)
    resources_count = serializers.SerializerMethodField()
    user_progress = serializers.SerializerMethodField()

    class Meta:
        model = TheoryTopic
        fields = ['id', 'name', 'description', 'level', 'level_id', 'content',
                 'order', 'is_active', 'resources_count', 'user_progress', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def get_resources_count(self, obj):
        return obj.resources.filter(is_active=True).count()

    def get_user_progress(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            try:
                progress = obj.user_progress.get(user=request.user)
                return {
                    'is_completed': progress.is_completed,
                    'completion_percentage': progress.completion_percentage,
                    'time_spent_minutes': progress.time_spent_minutes,
                    'last_accessed': progress.last_accessed
                }
            except UserProgress.DoesNotExist:
                return None
        return None


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['id', 'choice_text', 'is_correct', 'order']


class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)
    question_type_display = serializers.CharField(source='get_question_type_display', read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'question_type', 'question_type_display', 'question_text', 'explanation',
                 'order', 'points', 'audio_file', 'image', 'choices']


class TheoryTestSerializer(serializers.ModelSerializer):
    level = TheoryLevelSerializer(read_only=True)
    level_id = serializers.IntegerField(write_only=True)
    topic = TheoryTopicSerializer(read_only=True)
    topic_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    questions_count = serializers.SerializerMethodField()
    user_attempts_count = serializers.SerializerMethodField()
    best_score = serializers.SerializerMethodField()

    class Meta:
        model = TheoryTest
        fields = ['id', 'title', 'description', 'level', 'level_id', 'topic', 'topic_id',
                 'time_limit_minutes', 'passing_score', 'max_attempts', 'is_active',
                 'questions_count', 'user_attempts_count', 'best_score', 'created_at']
        read_only_fields = ['created_at']

    def get_questions_count(self, obj):
        return obj.questions.count()

    def get_user_attempts_count(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.attempts.filter(user=request.user).count()
        return 0

    def get_best_score(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            best_attempt = obj.attempts.filter(user=request.user).order_by('-score').first()
            return best_attempt.score if best_attempt else None
        return None


class AnswerSerializer(serializers.ModelSerializer):
    question = QuestionSerializer(read_only=True)
    selected_choice = ChoiceSerializer(read_only=True)

    class Meta:
        model = Answer
        fields = ['id', 'question', 'selected_choice', 'text_answer', 'is_correct', 'points_earned']


class TestAttemptSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    test = TheoryTestSerializer(read_only=True)
    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = TestAttempt
        fields = ['id', 'user', 'test', 'score', 'total_points', 'earned_points',
                 'started_at', 'completed_at', 'time_taken_minutes', 'is_passed', 'attempt_number']
        read_only_fields = ['id', 'score', 'total_points', 'earned_points', 'is_passed', 'attempt_number']


class TheoryResourceSerializer(serializers.ModelSerializer):
    topic = TheoryTopicSerializer(read_only=True)
    topic_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    resource_type_display = serializers.CharField(source='get_resource_type_display', read_only=True)

    class Meta:
        model = TheoryResource
        fields = ['id', 'title', 'description', 'resource_type', 'resource_type_display',
                 'topic', 'topic_id', 'file', 'url', 'duration_minutes', 'is_free', 'is_active', 'created_at']
        read_only_fields = ['id', 'created_at']


class UserProgressSerializer(serializers.ModelSerializer):
    topic = TheoryTopicSerializer(read_only=True)
    topic_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = UserProgress
        fields = ['id', 'topic', 'topic_id', 'is_completed', 'completion_percentage',
                 'time_spent_minutes', 'last_accessed', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate_completion_percentage(self, value):
        if value < 0 or value > 100:
            raise serializers.ValidationError("Completion percentage must be between 0 and 100")
        return value


class StudySessionSerializer(serializers.ModelSerializer):
    topic = TheoryTopicSerializer(read_only=True)
    topic_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = StudySession
        fields = ['id', 'topic', 'topic_id', 'user', 'start_time', 'end_time',
                 'duration_minutes', 'notes', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']


class SubmitTestSerializer(serializers.Serializer):
    """Serializer for submitting test answers"""
    answers = serializers.ListField(
        child=serializers.DictField(),
        min_length=1
    )

    def validate_answers(self, value):
        for answer in value:
            if 'question_id' not in answer:
                raise serializers.ValidationError("Each answer must have a question_id")
            if 'selected_choice_id' not in answer and 'text_answer' not in answer:
                raise serializers.ValidationError("Each answer must have either selected_choice_id or text_answer")
        return value


class SimpleTheoryTestSerializer(serializers.ModelSerializer):
    """Simplified serializer for lists"""
    level = TheoryLevelSerializer(read_only=True)
    questions_count = serializers.SerializerMethodField()

    class Meta:
        model = TheoryTest
        fields = ['id', 'title', 'level', 'time_limit_minutes', 'passing_score',
                 'max_attempts', 'questions_count', 'created_at']

    def get_questions_count(self, obj):
        return obj.questions.count()


class TheoryTopicDetailSerializer(TheoryTopicSerializer):
    """Extended topic serializer with related data"""
    resources = TheoryResourceSerializer(many=True, read_only=True)
    tests = SimpleTheoryTestSerializer(many=True, read_only=True)

    class Meta(TheoryTopicSerializer.Meta):
        fields = TheoryTopicSerializer.Meta.fields + ['resources', 'tests']
