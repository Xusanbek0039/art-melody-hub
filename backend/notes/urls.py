from django.urls import path
from . import views

urlpatterns = [
    path('categories/', views.CategoryListCreateView.as_view(), name='category-list'),
    path('categories/<int:pk>/', views.CategoryDetailView.as_view(), name='category-detail'),
    path('', views.NoteListCreateView.as_view(), name='note-list'),
    path('<int:pk>/', views.NoteDetailView.as_view(), name='note-detail'),
    path('<int:pk>/rate/', views.rate_note, name='rate-note'),
    path('<int:pk>/download/', views.download_note, name='download-note'),
    path('progress/', views.UserNoteProgressListCreateView.as_view(), name='progress-list'),
    path('progress/<int:pk>/', views.UserNoteProgressDetailView.as_view(), name='progress-detail'),
    path('practice/', views.PracticeSessionListCreateView.as_view(), name='practice-list'),
    path('practice/<int:pk>/', views.PracticeSessionDetailView.as_view(), name='practice-detail'),
    path('stats/', views.user_notes_stats, name='user-notes-stats'),
]
