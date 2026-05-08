from art_melody_hub.permissions import IsAdminOrReadOnly
from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Q, Avg, Count, Sum
from django.contrib.auth import get_user_model
from decimal import Decimal
from .models import (
    ProductCategory, Product, ProductRating, ProductLike, Cart, CartItem,
    Order, OrderItem, DeliveryFee, Wishlist
)
from .serializers import (
    ProductCategorySerializer, ProductSerializer, SimpleProductSerializer,
    ProductRatingSerializer, CartSerializer, CartItemSerializer,
    OrderSerializer, CreateOrderSerializer, DeliveryFeeSerializer,
    WishlistSerializer, UserOrderSerializer
)

User = get_user_model()


class ProductCategoryListCreateView(generics.ListCreateAPIView):
    """List and create product categories"""
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
    permission_classes = [IsAdminOrReadOnly]


class ProductCategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a product category"""
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
    permission_classes = [IsAdminOrReadOnly]


class ProductListCreateView(generics.ListCreateAPIView):
    """List and create products"""
    queryset = Product.objects.select_related('category', 'master').prefetch_related('ratings', 'likes')
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return SimpleProductSerializer
        return ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.select_related('category', 'master').prefetch_related('ratings', 'likes')
        
        # Filter by category
        category_id = self.request.query_params.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        
        # Filter by badge
        badge = self.request.query_params.get('badge')
        if badge:
            queryset = queryset.filter(badge=badge)
        
        # Filter by stock status
        in_stock = self.request.query_params.get('in_stock')
        if in_stock == 'true':
            queryset = queryset.filter(in_stock=True)
        
        # Filter by master
        master_id = self.request.query_params.get('master')
        if master_id:
            queryset = queryset.filter(master_id=master_id)
        
        # Search by name
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(name__icontains=search)
        
        # Filter featured
        featured = self.request.query_params.get('featured')
        if featured == 'true':
            queryset = queryset.filter(is_featured=True)
        
        # Sort options
        sort_by = self.request.query_params.get('sort', 'created_at')
        if sort_by == 'price_low':
            queryset = queryset.order_by('price')
        elif sort_by == 'price_high':
            queryset = queryset.order_by('-price')
        elif sort_by == 'rating':
            queryset = queryset.annotate(
                avg_rating=Avg('ratings__rating')
            ).order_by('-avg_rating')
        elif sort_by == 'popular':
            queryset = queryset.order_by('-orders_count', '-views_count')
        elif sort_by == 'newest':
            queryset = queryset.order_by('-created_at')
        else:
            queryset = queryset.order_by('-created_at')
        
        return queryset.filter(is_active=True)

    def perform_create(self, serializer):
        serializer.save(master=self.request.user)


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a product"""
    queryset = Product.objects.select_related('category', 'master').prefetch_related('ratings', 'likes')
    serializer_class = ProductSerializer
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
def rate_product(request, pk):
    """Rate a product"""
    try:
        product = Product.objects.get(pk=pk)
        rating, created = ProductRating.objects.get_or_create(
            user=request.user,
            product=product,
            defaults={
                'rating': request.data.get('rating', 5),
                'review': request.data.get('review', '')
            }
        )
        
        if not created:
            rating.rating = request.data.get('rating', rating.rating)
            rating.review = request.data.get('review', rating.review)
            rating.save()
        
        return Response(ProductRatingSerializer(rating).data)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def like_product(request, pk):
    """Like/unlike a product"""
    try:
        product = Product.objects.get(pk=pk)
        like, created = ProductLike.objects.get_or_create(
            user=request.user,
            product=product
        )
        
        if not created:
            # Unlike
            like.delete()
            product.likes_count -= 1
            action = 'unliked'
        else:
            # Like
            product.likes_count += 1
            action = 'liked'
        
        product.save(update_fields=['likes_count'])
        
        return Response({
            'action': action,
            'likes_count': product.likes_count
        })
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)


class CartView(generics.RetrieveUpdateAPIView):
    """Get and update user cart"""
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        return cart


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def add_to_cart(request):
    """Add item to cart"""
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    product_id = request.data.get('product_id')
    quantity = request.data.get('quantity', 1)
    
    try:
        product = Product.objects.get(id=product_id, is_active=True, in_stock=True)
        
        if product.stock_quantity < quantity:
            return Response({'error': 'Not enough stock'}, status=status.HTTP_400_BAD_REQUEST)
        
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity}
        )
        
        if not created:
            cart_item.quantity += quantity
            if cart_item.quantity > product.stock_quantity:
                return Response({'error': 'Not enough stock'}, status=status.HTTP_400_BAD_REQUEST)
            cart_item.save()
        
        return Response(CartItemSerializer(cart_item).data, status=status.HTTP_201_CREATED)
    
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated])
def update_cart_item(request, item_id):
    """Update cart item quantity"""
    try:
        cart_item = CartItem.objects.get(id=item_id, cart__user=request.user)
        quantity = request.data.get('quantity', 1)
        
        if quantity < 1:
            return Response({'error': 'Quantity must be at least 1'}, status=status.HTTP_400_BAD_REQUEST)
        
        if cart_item.product.stock_quantity < quantity:
            return Response({'error': 'Not enough stock'}, status=status.HTTP_400_BAD_REQUEST)
        
        cart_item.quantity = quantity
        cart_item.save()
        
        return Response(CartItemSerializer(cart_item).data)
    
    except CartItem.DoesNotExist:
        return Response({'error': 'Cart item not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def remove_from_cart(request, item_id):
    """Remove item from cart"""
    try:
        cart_item = CartItem.objects.get(id=item_id, cart__user=request.user)
        cart_item.delete()
        return Response({'message': 'Item removed from cart'})
    
    except CartItem.DoesNotExist:
        return Response({'error': 'Cart item not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_order(request):
    """Create order from cart"""
    try:
        cart = Cart.objects.get(user=request.user)
        if not cart.items.exists():
            return Response({'error': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = CreateOrderSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            
            # Calculate totals
            subtotal = cart.total_price
            
            # Get delivery fee
            try:
                delivery_fee_obj = DeliveryFee.objects.get(region=data['region'], is_active=True)
                delivery_fee = delivery_fee_obj.fee
                if subtotal >= delivery_fee_obj.free_delivery_threshold:
                    delivery_fee = 0
            except DeliveryFee.DoesNotExist:
                delivery_fee = 0
            
            total_amount = subtotal + delivery_fee
            
            # Create order
            order = Order.objects.create(
                user=request.user,
                customer_name=data['customer_name'],
                customer_phone=data['customer_phone'],
                customer_email=data.get('customer_email', ''),
                region=data['region'],
                address=data['address'],
                notes=data.get('notes', ''),
                payment_method=data['payment_method'],
                payment_provider=data.get('payment_provider', ''),
                subtotal=subtotal,
                delivery_fee=delivery_fee,
                total_amount=total_amount
            )
            
            # Create order items
            for cart_item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    product_name=cart_item.product.name,
                    product_price=cart_item.product.price,
                    product_image=cart_item.product.image.url if cart_item.product.image else '',
                    quantity=cart_item.quantity,
                    subtotal=cart_item.subtotal
                )
                
                # Update product orders count and stock
                product = cart_item.product
                product.orders_count += cart_item.quantity
                product.stock_quantity -= cart_item.quantity
                product.save()
            
            # Clear cart
            cart.items.all().delete()
            
            return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    except Cart.DoesNotExist:
        return Response({'error': 'Cart not found'}, status=status.HTTP_404_NOT_FOUND)


class OrderListCreateView(generics.ListCreateAPIView):
    """List and create orders"""
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.select_related('user').prefetch_related('items').all()
        return Order.objects.filter(user=self.request.user).select_related('user').prefetch_related('items')

    def get_serializer_class(self):
        if self.request.method == 'GET' and not self.request.user.is_staff:
            return UserOrderSerializer
        return OrderSerializer


class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete an order"""
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.select_related('user').prefetch_related('items').all()
        return Order.objects.filter(user=self.request.user).select_related('user').prefetch_related('items')


class DeliveryFeeListCreateView(generics.ListCreateAPIView):
    """List and create delivery fees"""
    queryset = DeliveryFee.objects.all()
    serializer_class = DeliveryFeeSerializer
    permission_classes = [permissions.IsAdminUser]


class DeliveryFeeDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete delivery fee"""
    queryset = DeliveryFee.objects.all()
    serializer_class = DeliveryFeeSerializer
    permission_classes = [permissions.IsAdminUser]


class WishlistListCreateView(generics.ListCreateAPIView):
    """List and create wishlist items"""
    serializer_class = WishlistSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user).select_related('product')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class WishlistDetailView(generics.RetrieveDestroyAPIView):
    """Retrieve or delete wishlist item"""
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user)


@api_view(['GET'])
@permission_classes([IsAdminOrReadOnly])
def market_stats(request):
    """Get market statistics"""
    total_products = Product.objects.filter(is_active=True).count()
    in_stock_products = Product.objects.filter(is_active=True, in_stock=True).count()
    total_orders = Order.objects.count()
    total_revenue = Order.objects.aggregate(
        total=Sum('total_amount')
    )['total'] or 0
    
    # Products by category
    products_by_category = ProductCategory.objects.annotate(
        count=Count('products', filter=Q(products__is_active=True))
    ).filter(count__gt=0).order_by('-count')
    
    # Top rated products
    top_products = Product.objects.filter(
        is_active=True,
        ratings__isnull=False
    ).annotate(
        avg_rating=Avg('ratings__rating')
    ).order_by('-avg_rating')[:5]
    
    return Response({
        'total_products': total_products,
        'in_stock_products': in_stock_products,
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'products_by_category': ProductCategorySerializer(products_by_category, many=True).data,
        'top_products': SimpleProductSerializer(top_products, many=True).data
    })


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_delivery_fee(request):
    """Get delivery fee for a region"""
    region = request.query_params.get('region')
    cart_total = Decimal(request.query_params.get('cart_total', '0'))
    
    if not region:
        return Response({'error': 'Region is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        delivery_fee_obj = DeliveryFee.objects.get(region=region, is_active=True)
        fee = delivery_fee_obj.fee
        if cart_total >= delivery_fee_obj.free_delivery_threshold:
            fee = 0
        
        return Response({
            'region': region,
            'fee': fee,
            'free_delivery_threshold': delivery_fee_obj.free_delivery_threshold,
            'remaining_for_free': max(0, delivery_fee_obj.free_delivery_threshold - cart_total)
        })
    
    except DeliveryFee.DoesNotExist:
        return Response({'fee': 0, 'free_delivery_threshold': 0, 'remaining_for_free': 0})
