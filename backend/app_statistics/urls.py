from django.urls import path
from . import views

urlpatterns = [
    path('activities/', views.UserActivityListCreateView.as_view(), name='user-activity-list'),
    path('daily-stats/', views.DailyStatsListCreateView.as_view(), name='daily-stats-list'),
    path('popular-content/', views.PopularContentListCreateView.as_view(), name='popular-content-list'),
    path('engagement/', views.UserEngagementDetailView.as_view(), name='user-engagement'),
    path('learning-paths/', views.LearningPathListCreateView.as_view(), name='learning-path-list'),
    path('learning-paths/<int:pk>/', views.LearningPathDetailView.as_view(), name='learning-path-detail'),
    path('learning-path-items/', views.LearningPathItemListCreateView.as_view(), name='learning-path-item-list'),
    path('metrics/', views.PerformanceMetricListCreateView.as_view(), name='performance-metric-list'),
    path('dashboard/', views.dashboard_stats, name='dashboard-stats'),
    path('user/', views.user_stats, name='user-stats'),
    path('content/', views.content_analytics, name='content-analytics'),
    path('learning/', views.learning_analytics, name='learning-analytics'),
    path('track/', views.track_activity, name='track-activity'),
]
