from art_melody_hub.permissions import IsAdminOrReadOnly
from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Q, Avg
from django.contrib.auth import get_user_model
from .models import (
    InstrumentCategory, Master, MasterReview, MasterWork,
    InstrumentAccessory, RepairService, Consultation
)
from .serializers import (
    InstrumentCategorySerializer, MasterSerializer, MasterReviewSerializer,
    MasterWorkSerializer, InstrumentAccessorySerializer, RepairServiceSerializer,
    ConsultationSerializer, SimpleMasterSerializer, MasterDetailSerializer
)

User = get_user_model()


class InstrumentCategoryListCreateView(generics.ListCreateAPIView):
    """List and create instrument categories"""
    queryset = InstrumentCategory.objects.all()
    serializer_class = InstrumentCategorySerializer
    permission_classes = [IsAdminOrReadOnly]


class InstrumentCategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete an instrument category"""
    queryset = InstrumentCategory.objects.all()
    serializer_class = InstrumentCategorySerializer
    permission_classes = [IsAdminOrReadOnly]


class MasterListCreateView(generics.ListCreateAPIView):
    """List and create masters"""
    queryset = Master.objects.select_related('user').prefetch_related('reviews', 'works')
    serializer_class = MasterSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return SimpleMasterSerializer
        return MasterSerializer

    def get_queryset(self):
        queryset = Master.objects.select_related('user').prefetch_related('reviews', 'works')
        
        # Filter by location
        location = self.request.query_params.get('location')
        if location:
            queryset = queryset.filter(location__icontains=location)
        
        # Filter by specialization
        specialization = self.request.query_params.get('specialization')
        if specialization:
            queryset = queryset.filter(specialization__icontains=specialization)
        
        # Filter by verification status
        verified = self.request.query_params.get('verified')
        if verified == 'true':
            queryset = queryset.filter(is_verified=True)
        
        # Search by business name or specialization
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(business_name__icontains=search) | 
                Q(specialization__icontains=search) |
                Q(user__first_name__icontains=search) |
                Q(user__last_name__icontains=search)
            )
        
        # Sort options
        sort_by = self.request.query_params.get('sort', 'created_at')
        if sort_by == 'rating':
            queryset = queryset.annotate(
                avg_rating=Avg('reviews__rating')
            ).order_by('-avg_rating')
        elif sort_by == 'experience':
            queryset = queryset.order_by('-experience_years')
        elif sort_by == 'reviews':
            queryset = queryset.order_by('-reviews_count')
        else:
            queryset = queryset.order_by('-created_at')
        
        return queryset


class MasterDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a master"""
    queryset = Master.objects.select_related('user').prefetch_related(
        'reviews', 'works', 'accessories', 'repair_services'
    )
    serializer_class = MasterDetailSerializer
    permission_classes = [IsAdminOrReadOnly]


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def review_master(request, pk):
    """Review a master"""
    try:
        master = Master.objects.get(pk=pk)
        review, created = MasterReview.objects.get_or_create(
            user=request.user,
            master=master,
            defaults={
                'rating': request.data.get('rating', 5),
                'review': request.data.get('review', '')
            }
        )
        
        if not created:
            review.rating = request.data.get('rating', review.rating)
            review.review = request.data.get('review', review.review)
            review.save()
        
        # Update master's rating
        reviews = master.reviews.all()
        if reviews:
            master.rating = sum(review.rating for review in reviews) / len(reviews)
            master.reviews_count = reviews.count()
            master.save()
        
        return Response(MasterReviewSerializer(review).data)
    except Master.DoesNotExist:
        return Response({'error': 'Master not found'}, status=status.HTTP_404_NOT_FOUND)


class MasterWorkListCreateView(generics.ListCreateAPIView):
    """List and create master works"""
    serializer_class = MasterWorkSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        master_id = self.request.query_params.get('master')
        if master_id:
            return MasterWork.objects.filter(master_id=master_id).select_related('master')
        return MasterWork.objects.select_related('master').all()


class MasterWorkDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a master work"""
    queryset = MasterWork.objects.select_related('master')
    serializer_class = MasterWorkSerializer
    permission_classes = [IsAdminOrReadOnly]


class InstrumentAccessoryListCreateView(generics.ListCreateAPIView):
    """List and create instrument accessories"""
    serializer_class = InstrumentAccessorySerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        queryset = InstrumentAccessory.objects.select_related('category', 'master')
        
        # Filter by category
        category_id = self.request.query_params.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        
        # Filter by master
        master_id = self.request.query_params.get('master')
        if master_id:
            queryset = queryset.filter(master_id=master_id)
        
        # Filter by stock status
        in_stock = self.request.query_params.get('in_stock')
        if in_stock == 'true':
            queryset = queryset.filter(in_stock=True)
        
        # Search by name
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(name__icontains=search)
        
        return queryset


class InstrumentAccessoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete an instrument accessory"""
    queryset = InstrumentAccessory.objects.select_related('category', 'master')
    serializer_class = InstrumentAccessorySerializer
    permission_classes = [IsAdminOrReadOnly]


class RepairServiceListCreateView(generics.ListCreateAPIView):
    """List and create repair services"""
    serializer_class = RepairServiceSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        queryset = RepairService.objects.select_related('master')
        
        # Filter by master
        master_id = self.request.query_params.get('master')
        if master_id:
            queryset = queryset.filter(master_id=master_id)
        
        # Filter by instrument type
        instrument_type = self.request.query_params.get('instrument_type')
        if instrument_type:
            queryset = queryset.filter(instrument_type__icontains=instrument_type)
        
        return queryset


class RepairServiceDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a repair service"""
    queryset = RepairService.objects.select_related('master')
    serializer_class = RepairServiceSerializer
    permission_classes = [IsAdminOrReadOnly]


class ConsultationListCreateView(generics.ListCreateAPIView):
    """List and create consultation requests"""
    serializer_class = ConsultationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Consultation.objects.select_related('master', 'user').all()
        return Consultation.objects.filter(user=self.request.user).select_related('master', 'user')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ConsultationDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a consultation request"""
    serializer_class = ConsultationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Consultation.objects.select_related('master', 'user').all()
        return Consultation.objects.filter(user=self.request.user).select_related('master', 'user')


@api_view(['GET'])
@permission_classes([IsAdminOrReadOnly])
def masters_stats(request):
    """Get masters statistics"""
    total_masters = Master.objects.count()
    verified_masters = Master.objects.filter(is_verified=True).count()
    total_reviews = MasterReview.objects.count()
    avg_rating = MasterReview.objects.aggregate(avg_rating=Avg('rating'))['avg_rating'] or 0
    
    # Masters by location
    masters_by_location = Master.objects.values('location').annotate(
        count=models.Count('id')
    ).order_by('-count')[:10]
    
    return Response({
        'total_masters': total_masters,
        'verified_masters': verified_masters,
        'total_reviews': total_reviews,
        'average_rating': round(avg_rating, 2),
        'masters_by_location': list(masters_by_location)
    })
