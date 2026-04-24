from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import (
    ProductCategory, Product, ProductRating, ProductLike, Cart, CartItem,
    Order, OrderItem, DeliveryFee, Wishlist
)

User = get_user_model()


class ProductCategorySerializer(serializers.ModelSerializer):
    products_count = serializers.SerializerMethodField()

    class Meta:
        model = ProductCategory
        fields = ['id', 'name', 'description', 'icon', 'products_count', 'created_at']

    def get_products_count(self, obj):
        return obj.products.filter(is_active=True, in_stock=True).count()


class ProductSerializer(serializers.ModelSerializer):
    category = ProductCategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)
    master = serializers.StringRelatedField(read_only=True)
    master_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    average_rating = serializers.FloatField(read_only=True)
    reviews_count = serializers.IntegerField(read_only=True)
    is_liked_by_user = serializers.SerializerMethodField()
    is_in_cart = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'category', 'category_id', 'price', 'old_price',
                 'badge', 'in_stock', 'stock_quantity', 'image', 'images', 'master', 'master_id',
                 'is_handmade', 'materials', 'dimensions', 'weight', 'care_instructions',
                 'shipping_info', 'views_count', 'likes_count', 'orders_count', 'is_featured',
                 'is_active', 'average_rating', 'reviews_count', 'is_liked_by_user', 'is_in_cart',
                 'created_at', 'updated_at']
        read_only_fields = ['views_count', 'likes_count', 'orders_count', 'created_at', 'updated_at']

    def get_is_liked_by_user(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(user=request.user).exists()
        return False

    def get_is_in_cart(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            try:
                cart = request.user.cart
                return cart.items.filter(product=obj).exists()
            except Cart.DoesNotExist:
                return False
        return False


class SimpleProductSerializer(serializers.ModelSerializer):
    """Simplified serializer for lists"""
    category = ProductCategorySerializer(read_only=True)
    average_rating = serializers.FloatField(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'category', 'price', 'old_price', 'badge', 'image',
                 'in_stock', 'is_featured', 'average_rating', 'created_at']


class ProductRatingSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    product = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = ProductRating
        fields = ['id', 'product', 'user', 'rating', 'review', 'is_verified_purchase', 'created_at']
        read_only_fields = ['id', 'is_verified_purchase', 'created_at']

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5")
        return value


class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer(read_only=True)
    product_id = serializers.IntegerField(write_only=True)
    subtotal = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_id', 'quantity', 'subtotal', 'created_at', 'updated_at']
        read_only_fields = ['id', 'subtotal', 'created_at', 'updated_at']

    def validate_product_id(self, value):
        try:
            product = Product.objects.get(id=value, is_active=True, in_stock=True)
        except Product.DoesNotExist:
            raise serializers.ValidationError("Product not available")
        return value

    def validate_quantity(self, value):
        if value < 1:
            raise serializers.ValidationError("Quantity must be at least 1")
        return value


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    total_items = serializers.IntegerField(read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_price', 'total_items', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class OrderItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'product_price', 'product_image',
                 'quantity', 'subtotal']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'order_number', 'user', 'customer_name', 'customer_phone',
                 'customer_email', 'region', 'address', 'notes', 'status', 'payment_method',
                 'payment_provider', 'is_paid', 'subtotal', 'delivery_fee', 'total_amount',
                 'tracking_number', 'estimated_delivery', 'items', 'created_at', 'updated_at']
        read_only_fields = ['id', 'order_number', 'subtotal', 'delivery_fee', 'total_amount',
                          'created_at', 'updated_at']


class CreateOrderSerializer(serializers.Serializer):
    """Serializer for creating orders from cart"""
    customer_name = serializers.CharField(max_length=100)
    customer_phone = serializers.CharField(max_length=20)
    customer_email = serializers.EmailField(required=False, allow_blank=True)
    region = serializers.CharField(max_length=100)
    address = serializers.CharField(max_length=500)
    notes = serializers.CharField(required=False, allow_blank=True, max_length=1000)
    payment_method = serializers.ChoiceField(choices=Order.PAYMENT_CHOICES)
    payment_provider = serializers.CharField(required=False, allow_blank=True, max_length=20)


class DeliveryFeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryFee
        fields = ['id', 'region', 'fee', 'free_delivery_threshold', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class WishlistSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer(read_only=True)
    product_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Wishlist
        fields = ['id', 'product', 'product_id', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate_product_id(self, value):
        try:
            Product.objects.get(id=value, is_active=True)
        except Product.DoesNotExist:
            raise serializers.ValidationError("Product not found")
        return value


class UserOrderSerializer(serializers.ModelSerializer):
    """Serializer for user's own orders"""
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'order_number', 'status', 'payment_method', 'is_paid',
                 'subtotal', 'delivery_fee', 'total_amount', 'tracking_number',
                 'estimated_delivery', 'items', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
