from django.urls import path
from . import views

urlpatterns = [
    path('levels/', views.TheoryLevelListCreateView.as_view(), name='theory-level-list'),
    path('levels/<int:pk>/', views.TheoryLevelDetailView.as_view(), name='theory-level-detail'),
    path('topics/', views.TheoryTopicListCreateView.as_view(), name='theory-topic-list'),
    path('topics/<int:pk>/', views.TheoryTopicDetailView.as_view(), name='theory-topic-detail'),
    path('tests/', views.TheoryTestListCreateView.as_view(), name='theory-test-list'),
    path('tests/<int:pk>/', views.TheoryTestDetailView.as_view(), name='theory-test-detail'),
    path('tests/<int:pk>/questions/', views.get_test_questions, name='get-test-questions'),
    path('tests/<int:pk>/submit/', views.submit_test, name='submit-test'),
    path('attempts/', views.TestAttemptListCreateView.as_view(), name='test-attempt-list'),
    path('attempts/<int:pk>/', views.TestAttemptDetailView.as_view(), name='test-attempt-detail'),
    path('resources/', views.TheoryResourceListCreateView.as_view(), name='theory-resource-list'),
    path('resources/<int:pk>/', views.TheoryResourceDetailView.as_view(), name='theory-resource-detail'),
    path('progress/', views.UserProgressListCreateView.as_view(), name='user-progress-list'),
    path('progress/<int:pk>/', views.UserProgressDetailView.as_view(), name='user-progress-detail'),
    path('sessions/', views.StudySessionListCreateView.as_view(), name='study-session-list'),
    path('sessions/<int:pk>/', views.StudySessionDetailView.as_view(), name='study-session-detail'),
    path('stats/', views.theory_stats, name='theory-stats'),
]
