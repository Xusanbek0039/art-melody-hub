from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Q, Count, Sum, Avg, F, Window
from django.db.models.functions import TruncDate, TruncDay, Rank
from django.utils import timezone
from datetime import timedelta, date
from django.contrib.auth import get_user_model
from decimal import Decimal
import json

from .models import (
    UserActivity, DailyStats, PopularContent, UserEngagement,
    LearningPath, LearningPathItem, PerformanceMetric
)
from .serializers import (
    UserActivitySerializer, DailyStatsSerializer, PopularContentSerializer,
    UserEngagementSerializer, LearningPathSerializer, LearningPathItemSerializer,
    PerformanceMetricSerializer, DashboardStatsSerializer, UserStatsSerializer,
    ContentAnalyticsSerializer, LearningAnalyticsSerializer
)

User = get_user_model()


class UserActivityListCreateView(generics.ListCreateAPIView):
    """List and create user activities"""
    serializer_class = UserActivitySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = UserActivity.objects.filter(user=self.request.user)
        
        # Filter by activity type
        activity_type = self.request.query_params.get('type')
        if activity_type:
            queryset = queryset.filter(activity_type=activity_type)
        
        # Filter by date range
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if start_date:
            queryset = queryset.filter(timestamp__date__gte=start_date)
        if end_date:
            queryset = queryset.filter(timestamp__date__lte=end_date)
        
        return queryset.order_by('-timestamp')

    def perform_create(self, serializer):
        # Get client info
        request = self.context.get('request')
        client_ip = self.get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')[:500] if request else ''
        
        serializer.save(
            user=self.request.user,
            ip_address=client_ip,
            user_agent=user_agent
        )

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class DailyStatsListCreateView(generics.ListCreateAPIView):
    """List and create daily statistics"""
    queryset = DailyStats.objects.all()
    serializer_class = DailyStatsSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        queryset = DailyStats.objects.all()
        
        # Filter by date range
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)
        
        return queryset.order_by('-date')


class PopularContentListCreateView(generics.ListCreateAPIView):
    """List and create popular content tracking"""
    serializer_class = PopularContentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = PopularContent.objects.all()
        
        # Filter by content type
        content_type = self.request.query_params.get('type')
        if content_type:
            queryset = queryset.filter(content_type=content_type)
        
        # Sort by different metrics
        sort_by = self.request.query_params.get('sort', 'views_count')
        if sort_by in ['views_count', 'likes_count', 'downloads_count', 'shares_count']:
            queryset = queryset.order_by(f'-{sort_by}')
        
        return queryset


class UserEngagementDetailView(generics.RetrieveUpdateAPIView):
    """Get and update user engagement metrics"""
    serializer_class = UserEngagementSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        engagement, created = UserEngagement.objects.get_or_create(user=self.request.user)
        return engagement


class LearningPathListCreateView(generics.ListCreateAPIView):
    """List and create learning paths"""
    serializer_class = LearningPathSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return LearningPath.objects.filter(user=self.request.user).prefetch_related('items')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class LearningPathDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a learning path"""
    serializer_class = LearningPathSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return LearningPath.objects.filter(user=self.request.user).prefetch_related('items')


class LearningPathItemListCreateView(generics.ListCreateAPIView):
    """List and create learning path items"""
    serializer_class = LearningPathItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        path_id = self.request.query_params.get('path_id')
        if path_id:
            return LearningPathItem.objects.filter(learning_path_id=path_id, learning_path__user=self.request.user)
        return LearningPathItem.objects.filter(learning_path__user=self.request.user)

    def perform_create(self, serializer):
        path_id = serializer.validated_data.get('learning_path_id') or self.request.query_params.get('path_id')
        if path_id:
            try:
                learning_path = LearningPath.objects.get(id=path_id, user=self.request.user)
                serializer.save(learning_path=learning_path)
            except LearningPath.DoesNotExist:
                raise serializers.ValidationError('Learning path not found')


class PerformanceMetricListCreateView(generics.ListCreateAPIView):
    """List and create performance metrics"""
    queryset = PerformanceMetric.objects.all()
    serializer_class = PerformanceMetricSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        queryset = PerformanceMetric.objects.all()
        
        # Filter by metric name
        metric_name = self.request.query_params.get('metric')
        if metric_name:
            queryset = queryset.filter(metric_name=metric_name)
        
        # Filter by date range
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)
        
        return queryset.order_by('-date')


@api_view(['GET'])
@permission_classes([permissions.IsAdminUser])
def dashboard_stats(request):
    """Get dashboard statistics for admin"""
    today = timezone.now().date()
    
    # Today's stats
    today_stats = DailyStats.objects.filter(date=today).first()
    
    # Get or create today's stats
    if not today_stats:
        # Calculate today's stats from activities
        today_users = UserActivity.objects.filter(timestamp__date=today).values('user').distinct().count()
        new_users_today = User.objects.filter(date_joined__date=today).count()
        sessions_today = UserActivity.objects.filter(timestamp__date=today).count()
        
        today_stats = {
            'active_users': today_users,
            'new_users': new_users_today,
            'total_sessions': sessions_today,
            'total_practice_time_minutes': 0,
            'notes_downloaded': 0,
            'tests_completed': 0,
            'orders_placed': 0,
            'revenue': 0
        }
    else:
        today_stats = DailyStatsSerializer(today_stats).data
    
    # Total users
    total_users = User.objects.count()
    
    # Popular content
    popular_notes = PopularContent.objects.filter(
        content_type='note'
    ).order_by('-views_count')[:5].values('content_id', 'views_count', 'likes_count')
    
    popular_products = PopularContent.objects.filter(
        content_type='product'
    ).order_by('-views_count')[:5].values('content_id', 'views_count', 'likes_count')
    
    # User growth (last 30 days)
    thirty_days_ago = today - timedelta(days=30)
    user_growth = DailyStats.objects.filter(
        date__gte=thirty_days_ago
    ).order_by('date').values('date', 'new_users')
    
    # Revenue trend (last 30 days)
    revenue_trend = DailyStats.objects.filter(
        date__gte=thirty_days_ago
    ).order_by('date').values('date', 'revenue')
    
    data = {
        'total_users': total_users,
        'active_users_today': today_stats.get('active_users', 0),
        'new_users_today': today_stats.get('new_users', 0),
        'total_sessions_today': today_stats.get('total_sessions', 0),
        'total_practice_time_today': today_stats.get('total_practice_time_minutes', 0),
        'notes_downloaded_today': today_stats.get('notes_downloaded', 0),
        'tests_completed_today': today_stats.get('tests_completed', 0),
        'orders_placed_today': today_stats.get('orders_placed', 0),
        'revenue_today': today_stats.get('revenue', 0),
        'popular_notes': list(popular_notes),
        'popular_products': list(popular_products),
        'user_growth': list(user_growth),
        'revenue_trend': list(revenue_trend)
    }
    
    serializer = DashboardStatsSerializer(data)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_stats(request):
    """Get detailed statistics for the authenticated user"""
    user = request.user
    
    # Get or create engagement data
    engagement, created = UserEngagement.objects.get_or_create(user=user)
    
    # Recent activities
    recent_activities = UserActivity.objects.filter(
        user=user
    ).order_by('-timestamp')[:10].values('activity_type', 'activity_data', 'timestamp')
    
    # Learning progress
    from notes.models import UserNoteProgress
    from theory.models import UserProgress as TheoryUserProgress
    
    notes_progress = UserNoteProgress.objects.filter(user=user).aggregate(
        total=Count('id'),
        completed=Count('id', filter=Q(is_completed=True)),
        avg_completion=Avg('completion_percentage')
    )
    
    theory_progress = TheoryUserProgress.objects.filter(user=user).aggregate(
        total=Count('id'),
        completed=Count('id', filter=Q(is_completed=True)),
        avg_completion=Avg('completion_percentage')
    )
    
    learning_progress = {
        'notes': notes_progress,
        'theory': theory_progress
    }
    
    # Achievements
    from accounts.models import Achievement
    achievements = Achievement.objects.filter(user=user).values('title', 'description', 'icon')
    
    data = {
        'total_practice_time': engagement.total_practice_time_minutes,
        'total_sessions': engagement.total_sessions,
        'notes_viewed': engagement.total_notes_viewed,
        'notes_downloaded': engagement.total_notes_downloaded,
        'tests_taken': engagement.total_tests_taken,
        'tests_passed': engagement.total_tests_passed,
        'test_pass_rate': engagement.test_pass_rate,
        'orders_placed': engagement.total_orders_placed,
        'total_spent': engagement.total_spent,
        'streak_days': engagement.streak_days,
        'average_session_duration': engagement.average_session_duration,
        'recent_activities': list(recent_activities),
        'learning_progress': learning_progress,
        'achievements': list(achievements)
    }
    
    serializer = UserStatsSerializer(data)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly])
def content_analytics(request):
    """Get content analytics"""
    content_type = request.query_params.get('type', 'note')
    
    # Total metrics
    content_stats = PopularContent.objects.filter(content_type=content_type).aggregate(
        total_views=Sum('views_count'),
        total_likes=Sum('likes_count'),
        total_downloads=Sum('downloads_count')
    )
    
    # Engagement rate (likes/views * 100)
    total_views = content_stats['total_views'] or 0
    total_likes = content_stats['total_likes'] or 0
    engagement_rate = (total_likes / total_views * 100) if total_views > 0 else 0
    
    # Top performing content
    top_content = PopularContent.objects.filter(content_type=content_type).order_by('-views_count')[:10]
    
    # Views by category (if notes)
    views_by_category = {}
    if content_type == 'note':
        from notes.models import Note, Category
        category_stats = Note.objects.values('category__name').annotate(
            views=Sum('views_count')
        ).order_by('-views')
        views_by_category = {item['category__name']: item['views'] for item in category_stats}
    
    # Views by date (last 30 days)
    thirty_days_ago = timezone.now().date() - timedelta(days=30)
    views_by_date = []
    
    for i in range(30):
        date = thirty_days_ago + timedelta(days=i)
        views_by_date.append({
            'date': date.isoformat(),
            'views': 0  # This would be calculated from actual activity data
        })
    
    data = {
        'total_views': content_stats['total_views'] or 0,
        'total_likes': content_stats['total_likes'] or 0,
        'total_downloads': content_stats['total_downloads'] or 0,
        'engagement_rate': round(engagement_rate, 2),
        'top_performing_content': PopularContentSerializer(top_content, many=True).data,
        'views_by_category': views_by_category,
        'views_by_date': views_by_date,
        'user_demographics': {}  # This would require more complex analytics
    }
    
    serializer = ContentAnalyticsSerializer(data)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def learning_analytics(request):
    """Get learning analytics for the user"""
    user = request.user
    
    # Total learning time
    from theory.models import StudySession
    from notes.models import PracticeSession
    
    theory_time = StudySession.objects.filter(user=user).aggregate(
        total=Sum('duration_minutes')
    )['total'] or 0
    
    practice_time = PracticeSession.objects.filter(user=user).aggregate(
        total=Sum('duration_minutes')
    )['total'] or 0
    
    total_learning_time = theory_time + practice_time
    
    # Average session duration
    total_sessions = StudySession.objects.filter(user=user).count() + PracticeSession.objects.filter(user=user).count()
    avg_session_duration = (total_learning_time / total_sessions) if total_sessions > 0 else 0
    
    # Completion rates
    from theory.models import UserProgress as TheoryUserProgress
    from notes.models import UserNoteProgress
    
    theory_completion = TheoryUserProgress.objects.filter(user=user).aggregate(
        total=Count('id'),
        completed=Count('id', filter=Q(is_completed=True))
    )
    
    notes_completion = UserNoteProgress.objects.filter(user=user).aggregate(
        total=Count('id'),
        completed=Count('id', filter=Q(is_completed=True))
    )
    
    completion_rates = {
        'theory': (theory_completion['completed'] / theory_completion['total'] * 100) if theory_completion['total'] > 0 else 0,
        'notes': (notes_completion['completed'] / notes_completion['total'] * 100) if notes_completion['total'] > 0 else 0
    }
    
    # Popular topics
    popular_topics = StudySession.objects.filter(
        user=user,
        topic__isnull=False
    ).values('topic__name').annotate(
        sessions=Count('id'),
        total_time=Sum('duration_minutes')
    ).order_by('-total_time')[:5]
    
    # Difficulty distribution
    from theory.models import TheoryLevel
    difficulty_dist = TheoryUserProgress.objects.filter(
        user=user,
        topic__level__isnull=False
    ).values('topic__level__name').annotate(
        count=Count('id')
    ).order_by('topic__level__order')
    
    difficulty_distribution = {item['topic__level__name']: item['count'] for item in difficulty_dist}
    
    # Learning paths
    learning_paths_created = LearningPath.objects.filter(user=user).count()
    learning_paths_completed = LearningPath.objects.filter(user=user, is_completed=True).count()
    
    data = {
        'total_learning_time': total_learning_time,
        'average_session_duration': round(avg_session_duration, 2),
        'completion_rates': completion_rates,
        'popular_topics': list(popular_topics),
        'difficulty_distribution': difficulty_distribution,
        'learning_paths_created': learning_paths_created,
        'learning_paths_completed': learning_paths_completed
    }
    
    serializer = LearningAnalyticsSerializer(data)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def track_activity(request):
    """Track user activity"""
    activity_type = request.data.get('activity_type')
    activity_data = request.data.get('activity_data', {})
    
    if not activity_type:
        return Response({'error': 'activity_type is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Get client info
    client_ip = UserActivityListCreateView().get_client_ip(request)
    user_agent = request.META.get('HTTP_USER_AGENT', '')[:500]
    
    activity = UserActivity.objects.create(
        user=request.user,
        activity_type=activity_type,
        activity_data=activity_data,
        ip_address=client_ip,
        user_agent=user_agent
    )
    
    # Update engagement metrics
    engagement, created = UserEngagement.objects.get_or_create(user=request.user)
    
    if activity_type == 'login':
        engagement.last_login = timezone.now()
        engagement.total_sessions += 1
    elif activity_type == 'note_view':
        engagement.total_notes_viewed += 1
    elif activity_type == 'note_download':
        engagement.total_notes_downloaded += 1
    elif activity_type == 'test_taken':
        engagement.total_tests_taken += 1
    elif activity_type == 'test_passed':
        engagement.total_tests_passed += 1
    elif activity_type == 'order_placed':
        engagement.total_orders_placed += 1
    elif activity_type == 'practice_session':
        duration = activity_data.get('duration_minutes', 0)
        engagement.total_practice_time_minutes += duration
    
    engagement.save()
    
    return Response({'message': 'Activity tracked successfully'}, status=status.HTTP_201_CREATED)
