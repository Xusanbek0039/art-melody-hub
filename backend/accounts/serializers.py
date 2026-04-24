from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User, Profile, Achievement, CompetitionParticipation


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'phone', 
                 'region', 'address', 'bio', 'avatar', 'specialization', 'education', 
                 'is_master', 'created_at']
        read_only_fields = ['id', 'created_at']


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Profile
        fields = ['user', 'practice_time_hours', 'competitions_count', 'achievements_count',
                 'preferred_instrument', 'skill_level']


class AchievementSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Achievement
        fields = ['id', 'user', 'title', 'description', 'icon', 'earned_at']
        read_only_fields = ['id', 'earned_at']


class CompetitionParticipationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = CompetitionParticipation
        fields = ['id', 'user', 'competition_name', 'year', 'result', 'is_winner', 'certificate_url']
        read_only_fields = ['id']


class LoginSerializer(serializers.Serializer):
    email_or_phone = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email_or_phone = attrs.get('email_or_phone')
        password = attrs.get('password')

        if email_or_phone and password:
            # Try to authenticate with email first
            user = None
            try:
                if '@' in email_or_phone:
                    user = User.objects.get(email=email_or_phone)
                else:
                    user = User.objects.get(phone=email_or_phone)
                
                user = authenticate(username=user.username, password=password)
            except User.DoesNotExist:
                raise serializers.ValidationError('Invalid credentials')
            
            if not user:
                raise serializers.ValidationError('Invalid credentials')
            
            attrs['user'] = user
            return attrs
        else:
            raise serializers.ValidationError('Both email/phone and password are required')


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'phone', 
                 'password', 'confirm_password', 'region', 'specialization']

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError("Passwords don't match")
        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        
        # Create profile
        Profile.objects.create(user=user)
        
        return user
