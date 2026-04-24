from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import login, logout
from .models import User, Profile, Achievement, CompetitionParticipation
from .serializers import (
    UserSerializer, ProfileSerializer, AchievementSerializer,
    CompetitionParticipationSerializer, LoginSerializer, RegisterSerializer
)


class RegisterView(generics.CreateAPIView):
    """User registration endpoint"""
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Create token for the user
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'user': UserSerializer(user).data,
            'token': token.key,
            'message': 'Registration successful'
        }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_view(request):
    """User login endpoint"""
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        login(request, user)
        
        # Get or create token
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'user': UserSerializer(user).data,
            'token': token.key,
            'message': 'Login successful'
        })
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout_view(request):
    """User logout endpoint"""
    try:
        # Delete the token
        request.user.auth_token.delete()
        logout(request)
        return Response({'message': 'Logout successful'})
    except:
        return Response({'message': 'Logout successful'})


class ProfileView(generics.RetrieveUpdateAPIView):
    """Get and update user profile"""
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        return profile


class UserDetailView(generics.RetrieveUpdateAPIView):
    """Get and update user details"""
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class AchievementListCreateView(generics.ListCreateAPIView):
    """List and create achievements for the authenticated user"""
    serializer_class = AchievementSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Achievement.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AchievementDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete an achievement"""
    serializer_class = AchievementSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Achievement.objects.filter(user=self.request.user)


class CompetitionParticipationListCreateView(generics.ListCreateAPIView):
    """List and create competition participations for the authenticated user"""
    serializer_class = CompetitionParticipationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CompetitionParticipation.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CompetitionParticipationDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a competition participation"""
    serializer_class = CompetitionParticipationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CompetitionParticipation.objects.filter(user=self.request.user)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_stats(request):
    """Get user statistics"""
    profile = request.user.profile
    achievements = Achievement.objects.filter(user=request.user).count()
    competitions = CompetitionParticipation.objects.filter(user=request.user).count()
    wins = CompetitionParticipation.objects.filter(user=request.user, is_winner=True).count()
    
    return Response({
        'practice_time_hours': profile.practice_time_hours,
        'competitions_count': competitions,
        'achievements_count': achievements,
        'wins_count': wins,
        'skill_level': profile.skill_level,
        'preferred_instrument': profile.preferred_instrument
    })
