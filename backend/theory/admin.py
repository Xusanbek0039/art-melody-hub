from django.contrib import admin
from .models import (
    TheoryLevel, TheoryTopic, TheoryTest, Question, Choice,
    TestAttempt, Answer, TheoryResource, UserProgress, StudySession
)


@admin.register(TheoryLevel)
class TheoryLevelAdmin(admin.ModelAdmin):
    list_display = ['name', 'order', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['order']


@admin.register(TheoryTopic)
class TheoryTopicAdmin(admin.ModelAdmin):
    list_display = ['name', 'level', 'order', 'is_active', 'created_at']
    list_filter = ['level', 'is_active', 'created_at']
    search_fields = ['name', 'description', 'content']
    ordering = ['level', 'order']


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 4
    fields = ['choice_text', 'is_correct', 'order']


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['question_text', 'test', 'question_type', 'points', 'order']
    list_filter = ['question_type', 'points']
    search_fields = ['question_text', 'test__title']
    ordering = ['test', 'order']
    inlines = [ChoiceInline]


@admin.register(TheoryTest)
class TheoryTestAdmin(admin.ModelAdmin):
    list_display = ['title', 'level', 'topic', 'time_limit_minutes', 'passing_score', 'max_attempts', 'is_active']
    list_filter = ['level', 'topic', 'is_active', 'created_at']
    search_fields = ['title', 'description']
    ordering = ['-created_at']
    readonly_fields = ['created_at']


@admin.register(TestAttempt)
class TestAttemptAdmin(admin.ModelAdmin):
    list_display = ['user', 'test', 'score', 'is_passed', 'attempt_number', 'started_at']
    list_filter = ['is_passed', 'score', 'started_at']
    search_fields = ['user__username', 'test__title']
    ordering = ['-started_at']
    readonly_fields = ['score', 'total_points', 'earned_points', 'is_passed', 'started_at', 'completed_at']


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['attempt', 'question', 'is_correct', 'points_earned']
    list_filter = ['is_correct', 'points_earned']
    search_fields = ['attempt__user__username', 'question__question_text']
    ordering = ['-attempt__started_at']


@admin.register(TheoryResource)
class TheoryResourceAdmin(admin.ModelAdmin):
    list_display = ['title', 'resource_type', 'topic', 'is_free', 'is_active', 'created_at']
    list_filter = ['resource_type', 'is_free', 'is_active', 'created_at']
    search_fields = ['title', 'description', 'topic__name']
    ordering = ['-created_at']
    readonly_fields = ['created_at']


@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'topic', 'completion_percentage', 'is_completed', 'time_spent_minutes', 'last_accessed']
    list_filter = ['is_completed', 'last_accessed']
    search_fields = ['user__username', 'topic__name']
    ordering = ['-last_accessed']
    readonly_fields = ['created_at', 'last_accessed']


@admin.register(StudySession)
class StudySessionAdmin(admin.ModelAdmin):
    list_display = ['user', 'topic', 'duration_minutes', 'start_time', 'created_at']
    list_filter = ['duration_minutes', 'start_time', 'created_at']
    search_fields = ['user__username', 'topic__name', 'notes']
    ordering = ['-created_at']
    readonly_fields = ['created_at']
