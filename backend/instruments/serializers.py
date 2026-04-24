from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import (
    InstrumentCategory, Master, MasterReview, MasterWork,
    InstrumentAccessory, RepairService, Consultation
)

User = get_user_model()


class InstrumentCategorySerializer(serializers.ModelSerializer):
    masters_count = serializers.SerializerMethodField()
    accessories_count = serializers.SerializerMethodField()

    class Meta:
        model = InstrumentCategory
        fields = ['id', 'name', 'description', 'icon', 'masters_count', 'accessories_count', 'created_at']

    def get_masters_count(self, obj):
        return Master.objects.filter(user__is_active=True).count()

    def get_accessories_count(self, obj):
        return obj.accessories.filter(in_stock=True).count()


class MasterSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    average_rating = serializers.SerializerMethodField()
    works_count = serializers.SerializerMethodField()
    reviews_count = serializers.SerializerMethodField()
    is_reviewed_by_user = serializers.SerializerMethodField()

    class Meta:
        model = Master
        fields = ['id', 'user', 'business_name', 'specialization', 'experience_years',
                 'bio', 'location', 'phone', 'email', 'website', 'instagram', 'telegram',
                 'rating', 'reviews_count', 'is_verified', 'avatar', 'banner_image',
                 'average_rating', 'works_count', 'is_reviewed_by_user', 'created_at', 'updated_at']
        read_only_fields = ['rating', 'reviews_count', 'created_at', 'updated_at']

    def get_average_rating(self, obj):
        reviews = obj.reviews.all()
        if reviews:
            return sum(review.rating for review in reviews) / len(reviews)
        return obj.rating

    def get_works_count(self, obj):
        return obj.works.count()

    def get_reviews_count(self, obj):
        return obj.reviews.count()

    def get_is_reviewed_by_user(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.reviews.filter(user=request.user).exists()
        return False


class MasterReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    master = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = MasterReview
        fields = ['id', 'master', 'user', 'rating', 'review', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5")
        return value


class MasterWorkSerializer(serializers.ModelSerializer):
    master = MasterSerializer(read_only=True)
    master_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = MasterWork
        fields = ['id', 'master', 'master_id', 'title', 'description', 'image',
                 'instrument_type', 'price_range', 'is_featured', 'created_at']
        read_only_fields = ['id', 'created_at']


class InstrumentAccessorySerializer(serializers.ModelSerializer):
    category = InstrumentCategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)
    master = MasterSerializer(read_only=True)
    master_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = InstrumentAccessory
        fields = ['id', 'name', 'description', 'category', 'category_id', 'price',
                 'image', 'in_stock', 'master', 'master_id', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class RepairServiceSerializer(serializers.ModelSerializer):
    master = MasterSerializer(read_only=True)
    master_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = RepairService
        fields = ['id', 'master', 'master_id', 'instrument_type', 'service_name',
                 'description', 'price_range', 'duration_days', 'created_at']
        read_only_fields = ['id', 'created_at']


class ConsultationSerializer(serializers.ModelSerializer):
    master = MasterSerializer(read_only=True)
    master_id = serializers.IntegerField(write_only=True)
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Consultation
        fields = ['id', 'master', 'master_id', 'user', 'name', 'phone', 'email',
                 'message', 'consultation_type', 'is_contacted', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']


class SimpleMasterSerializer(serializers.ModelSerializer):
    """Simplified serializer for lists"""
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Master
        fields = ['id', 'user', 'business_name', 'specialization', 'location',
                 'rating', 'reviews_count', 'is_verified', 'avatar', 'created_at']


class MasterDetailSerializer(MasterSerializer):
    """Extended master serializer with related data"""
    works = MasterWorkSerializer(many=True, read_only=True)
    reviews = MasterReviewSerializer(many=True, read_only=True)
    accessories = InstrumentAccessorySerializer(many=True, read_only=True)
    repair_services = RepairServiceSerializer(many=True, read_only=True)

    class Meta(MasterSerializer.Meta):
        fields = MasterSerializer.Meta.fields + ['works', 'reviews', 'accessories', 'repair_services']
