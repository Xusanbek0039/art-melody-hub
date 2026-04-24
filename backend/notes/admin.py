from django.contrib import admin
from .models import Category, Note, NoteRating, UserNoteProgress, PracticeSession


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['name']


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ['title', 'composer', 'category', 'difficulty_level', 
                   'duration_minutes', 'views_count', 'downloads_count', 'is_featured', 'created_at']
    list_filter = ['difficulty_level', 'is_featured', 'category', 'created_at']
    search_fields = ['title', 'composer', 'description']
    ordering = ['-created_at']
    readonly_fields = ['views_count', 'downloads_count', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('title', 'composer', 'category', 'difficulty_level', 'description')
        }),
        ('Media Files', {
            'fields': ('pdf_file', 'audio_file', 'image', 'duration_minutes')
        }),
        ('Statistics', {
            'fields': ('views_count', 'downloads_count', 'is_featured')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(NoteRating)
class NoteRatingAdmin(admin.ModelAdmin):
    list_display = ['user', 'note', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['user__username', 'note__title', 'review']
    ordering = ['-created_at']


@admin.register(UserNoteProgress)
class UserNoteProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'note', 'is_completed', 'completion_percentage', 
                   'practice_time_minutes', 'last_practiced']
    list_filter = ['is_completed', 'last_practiced']
    search_fields = ['user__username', 'note__title']
    ordering = ['-updated_at']


@admin.register(PracticeSession)
class PracticeSessionAdmin(admin.ModelAdmin):
    list_display = ['user', 'note', 'duration_minutes', 'start_time', 'created_at']
    list_filter = ['duration_minutes', 'start_time', 'created_at']
    search_fields = ['user__username', 'note__title', 'notes']
    ordering = ['-created_at']
    date_hierarchy = 'start_time'
