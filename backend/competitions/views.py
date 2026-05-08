from art_melody_hub.permissions import IsAdminOrReadOnly
from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Q, Count
from django.utils import timezone
from .models import (
    Competition, CompetitionCategory, Registration, Result,
    Judge, Schedule, News
)
from .serializers import (
    CompetitionSerializer, SimpleCompetitionSerializer, CompetitionCategorySerializer,
    RegistrationSerializer, UserRegistrationSerializer, ResultSerializer,
    JudgeSerializer, ScheduleSerializer, NewsSerializer
)


class CompetitionListCreateView(generics.ListCreateAPIView):
    """List and create competitions"""
    queryset = Competition.objects.prefetch_related('categories', 'registrations')
    serializer_class = CompetitionSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return SimpleCompetitionSerializer
        return CompetitionSerializer

    def get_queryset(self):
        queryset = Competition.objects.prefetch_related('categories', 'registrations')
        
        # Filter by status
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # Filter by level
        level = self.request.query_params.get('level')
        if level:
            queryset = queryset.filter(level=level)
        
        # Filter by registration open
        registration_open = self.request.query_params.get('registration_open')
        if registration_open == 'true':
            today = timezone.now().date()
            queryset = queryset.filter(
                registration_start__lte=today,
                registration_end__gte=today
            )
        
        # Search by title or location
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(location__icontains=search)
            )
        
        # Filter featured
        featured = self.request.query_params.get('featured')
        if featured == 'true':
            queryset = queryset.filter(is_featured=True)
        
        # Sort options
        sort_by = self.request.query_params.get('sort', 'start_date')
        if sort_by == 'start_date':
            queryset = queryset.order_by('start_date')
        elif sort_by == 'registration_end':
            queryset = queryset.order_by('registration_end')
        elif sort_by == 'created_at':
            queryset = queryset.order_by('-created_at')
        else:
            queryset = queryset.order_by('start_date')
        
        return queryset


class CompetitionDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a competition"""
    queryset = Competition.objects.prefetch_related('categories', 'registrations', 'judges', 'schedule', 'news')
    serializer_class = CompetitionSerializer
    permission_classes = [IsAdminOrReadOnly]


class CompetitionCategoryListCreateView(generics.ListCreateAPIView):
    """List and create competition categories"""
    serializer_class = CompetitionCategorySerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        competition_id = self.request.query_params.get('competition')
        if competition_id:
            return CompetitionCategory.objects.filter(competition_id=competition_id)
        return CompetitionCategory.objects.all()


class CompetitionCategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a competition category"""
    queryset = CompetitionCategory.objects.all()
    serializer_class = CompetitionCategorySerializer
    permission_classes = [IsAdminOrReadOnly]


class RegistrationListCreateView(generics.ListCreateAPIView):
    """List and create registrations"""
    serializer_class = RegistrationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Registration.objects.select_related('user', 'competition', 'category').all()
        return Registration.objects.filter(user=self.request.user).select_related('user', 'competition', 'category')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class RegistrationDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a registration"""
    serializer_class = RegistrationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Registration.objects.select_related('user', 'competition', 'category').all()
        return Registration.objects.filter(user=self.request.user).select_related('user', 'competition', 'category')


class UserRegistrationListView(generics.ListAPIView):
    """List current user's registrations with results"""
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Registration.objects.filter(user=self.request.user).select_related(
            'competition', 'category', 'result'
        ).prefetch_related('result')


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def submit_registration(request, competition_id, category_id):
    """Submit registration for a competition category"""
    try:
        competition = Competition.objects.get(pk=competition_id)
        category = CompetitionCategory.objects.get(pk=category_id, competition=competition)
        
        # Check if registration is open
        if not competition.is_registration_open:
            return Response({'error': 'Registration is not open'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if user already registered
        if Registration.objects.filter(user=request.user, competition=competition, category=category).exists():
            return Response({'error': 'Already registered for this category'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check max participants
        if category.max_participants:
            current_registrations = Registration.objects.filter(category=category).count()
            if current_registrations >= category.max_participants:
                return Response({'error': 'Category is full'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create registration
        registration = Registration.objects.create(
            user=request.user,
            competition=competition,
            category=category,
            piece_title=request.data.get('piece_title', ''),
            composer=request.data.get('composer', ''),
            duration_minutes=request.data.get('duration_minutes', 0),
            teacher_name=request.data.get('teacher_name', ''),
            teacher_phone=request.data.get('teacher_phone', ''),
            institution=request.data.get('institution', ''),
            experience_years=request.data.get('experience_years'),
            previous_achievements=request.data.get('previous_achievements', ''),
            special_needs=request.data.get('special_needs', ''),
            notes=request.data.get('notes', '')
        )
        
        return Response(UserRegistrationSerializer(registration).data, status=status.HTTP_201_CREATED)
    
    except Competition.DoesNotExist:
        return Response({'error': 'Competition not found'}, status=status.HTTP_404_NOT_FOUND)
    except CompetitionCategory.DoesNotExist:
        return Response({'error': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)


class ResultListCreateView(generics.ListCreateAPIView):
    """List and create results (admin only)"""
    serializer_class = ResultSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        return Result.objects.select_related('registration__user', 'registration__competition')


class ResultDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a result (admin only)"""
    queryset = Result.objects.select_related('registration__user', 'registration__competition')
    serializer_class = ResultSerializer
    permission_classes = [permissions.IsAdminUser]


class JudgeListCreateView(generics.ListCreateAPIView):
    """List and create judges"""
    serializer_class = JudgeSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        competition_id = self.request.query_params.get('competition')
        if competition_id:
            return Judge.objects.filter(competition_id=competition_id).order_by('order')
        return Judge.objects.all().order_by('order')


class JudgeDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a judge"""
    queryset = Judge.objects.all()
    serializer_class = JudgeSerializer
    permission_classes = [IsAdminOrReadOnly]


class ScheduleListCreateView(generics.ListCreateAPIView):
    """List and create schedule"""
    serializer_class = ScheduleSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        competition_id = self.request.query_params.get('competition')
        if competition_id:
            return Schedule.objects.filter(competition_id=competition_id).order_by('date', 'time')
        return Schedule.objects.all().order_by('date', 'time')


class ScheduleDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a schedule item"""
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    permission_classes = [IsAdminOrReadOnly]


class NewsListCreateView(generics.ListCreateAPIView):
    """List and create news"""
    serializer_class = NewsSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        competition_id = self.request.query_params.get('competition')
        if competition_id:
            return News.objects.filter(competition_id=competition_id).order_by('-created_at')
        return News.objects.all().order_by('-created_at')


class NewsDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete news"""
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [IsAdminOrReadOnly]


@api_view(['GET'])
@permission_classes([IsAdminOrReadOnly])
def competitions_stats(request):
    """Get competitions statistics"""
    total_competitions = Competition.objects.count()
    upcoming_competitions = Competition.objects.filter(status='upcoming').count()
    active_competitions = Competition.objects.filter(status='active').count()
    total_registrations = Registration.objects.count()
    
    # Competitions by level
    competitions_by_level = Competition.objects.values('level').annotate(
        count=Count('id')
    ).order_by('level')
    
    # Registration statistics
    pending_registrations = Registration.objects.filter(status='pending').count()
    approved_registrations = Registration.objects.filter(status='approved').count()
    
    return Response({
        'total_competitions': total_competitions,
        'upcoming_competitions': upcoming_competitions,
        'active_competitions': active_competitions,
        'total_registrations': total_registrations,
        'pending_registrations': pending_registrations,
        'approved_registrations': approved_registrations,
        'competitions_by_level': list(competitions_by_level)
    })
