from art_melody_hub.permissions import IsAdminOrReadOnly
from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Q, Avg
from django.utils import timezone
from .models import Category, Note, NoteRating, UserNoteProgress, PracticeSession
from .serializers import (
    CategorySerializer, NoteSerializer, NoteRatingSerializer,
    UserNoteProgressSerializer, PracticeSessionSerializer, SimpleNoteSerializer
)


class CategoryListCreateView(generics.ListCreateAPIView):
    """List and create note categories"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a category"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]


class NoteListCreateView(generics.ListCreateAPIView):
    """List and create notes"""
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return SimpleNoteSerializer
        return NoteSerializer

    def get_queryset(self):
        queryset = Note.objects.select_related('category').prefetch_related('ratings')
        
        # Filter by category
        category_id = self.request.query_params.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        
        # Filter by difficulty level
        difficulty = self.request.query_params.get('difficulty')
        if difficulty:
            queryset = queryset.filter(difficulty_level=difficulty)
        
        # Search by title or composer
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(composer__icontains=search)
            )
        
        # Filter featured notes
        featured = self.request.query_params.get('featured')
        if featured == 'true':
            queryset = queryset.filter(is_featured=True)
        
        # Sort options
        sort_by = self.request.query_params.get('sort', 'created_at')
        if sort_by == 'rating':
            queryset = queryset.annotate(
                avg_rating=Avg('ratings__rating')
            ).order_by('-avg_rating')
        elif sort_by == 'views':
            queryset = queryset.order_by('-views_count')
        elif sort_by == 'downloads':
            queryset = queryset.order_by('-downloads_count')
        else:
            queryset = queryset.order_by('-created_at')
        
        return queryset

    def perform_create(self, serializer):
        serializer.save()
        # Increment views when creating (for analytics)
        pass


class NoteDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a note"""
    queryset = Note.objects.select_related('category').prefetch_related('ratings')
    serializer_class = NoteSerializer
    permission_classes = [IsAdminOrReadOnly]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # Increment views count
        instance.views_count += 1
        instance.save(update_fields=['views_count'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def rate_note(request, pk):
    """Rate a note"""
    try:
        note = Note.objects.get(pk=pk)
        rating, created = NoteRating.objects.get_or_create(
            user=request.user,
            note=note,
            defaults={
                'rating': request.data.get('rating', 5),
                'review': request.data.get('review', '')
            }
        )
        
        if not created:
            rating.rating = request.data.get('rating', rating.rating)
            rating.review = request.data.get('review', rating.review)
            rating.save()
        
        return Response(NoteRatingSerializer(rating).data)
    except Note.DoesNotExist:
        return Response({'error': 'Note not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def download_note(request, pk):
    """Download a note (increment download count)"""
    try:
        note = Note.objects.get(pk=pk)
        note.downloads_count += 1
        note.save(update_fields=['downloads_count'])
        
        return Response({
            'message': 'Download count incremented',
            'download_url': note.pdf_file.url if note.pdf_file else None
        })
    except Note.DoesNotExist:
        return Response({'error': 'Note not found'}, status=status.HTTP_404_NOT_FOUND)


class UserNoteProgressListCreateView(generics.ListCreateAPIView):
    """List and create user note progress"""
    serializer_class = UserNoteProgressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserNoteProgress.objects.filter(user=self.request.user).select_related('note')

    def perform_create(self, serializer):
        note_id = serializer.validated_data.get('note_id')
        try:
            note = Note.objects.get(pk=note_id)
            progress, created = UserNoteProgress.objects.get_or_create(
                user=self.request.user,
                note=note,
                defaults=serializer.validated_data
            )
            
            if not created:
                # Update existing progress
                for key, value in serializer.validated_data.items():
                    if key != 'note_id':
                        setattr(progress, key, value)
                progress.save()
            
            return progress
        except Note.DoesNotExist:
            raise serializers.ValidationError({'note_id': 'Note not found'})


class UserNoteProgressDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete user note progress"""
    serializer_class = UserNoteProgressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserNoteProgress.objects.filter(user=self.request.user).select_related('note')


class PracticeSessionListCreateView(generics.ListCreateAPIView):
    """List and create practice sessions"""
    serializer_class = PracticeSessionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return PracticeSession.objects.filter(user=self.request.user).select_related('note')

    def perform_create(self, serializer):
        # Update user's total practice time
        duration = serializer.validated_data.get('duration_minutes', 0)
        if duration > 0:
            profile = self.request.user.profile
            profile.practice_time_hours += duration // 60
            profile.save(update_fields=['practice_time_hours'])
        
        serializer.save(user=self.request.user)


class PracticeSessionDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a practice session"""
    serializer_class = PracticeSessionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return PracticeSession.objects.filter(user=self.request.user).select_related('note')


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_notes_stats(request):
    """Get user's notes statistics"""
    total_notes = UserNoteProgress.objects.filter(user=request.user).count()
    completed_notes = UserNoteProgress.objects.filter(user=request.user, is_completed=True).count()
    total_practice_time = PracticeSession.objects.filter(user=request.user).aggregate(
        total=models.Sum('duration_minutes')
    )['total'] or 0
    
    # Get practice time by category
    practice_by_category = PracticeSession.objects.filter(
        user=request.user,
        note__isnull=False
    ).values('note__category__name').annotate(
        total_time=models.Sum('duration_minutes')
    ).order_by('-total_time')

    return Response({
        'total_notes': total_notes,
        'completed_notes': completed_notes,
        'total_practice_time_minutes': total_practice_time,
        'total_practice_time_hours': total_practice_time // 60,
        'practice_by_category': list(practice_by_category),
        'completion_rate': (completed_notes / total_notes * 100) if total_notes > 0 else 0
    })
