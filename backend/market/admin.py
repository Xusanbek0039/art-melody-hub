from django.contrib import admin
from .models import (
    ProductCategory, Product, ProductRating, ProductLike, Cart, CartItem,
    Order, OrderItem, DeliveryFee, Wishlist
)


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'old_price', 'badge', 'in_stock',
                   'stock_quantity', 'is_featured', 'is_active', 'master', 'created_at']
    list_filter = ['category', 'badge', 'in_stock', 'is_featured', 'is_active', 'created_at']
    search_fields = ['name', 'description', 'materials', 'master__username']
    ordering = ['-created_at']
    readonly_fields = ['views_count', 'likes_count', 'orders_count', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'description', 'category', 'price', 'old_price', 'badge')
        }),
        ('Stock & Status', {
            'fields': ('in_stock', 'stock_quantity', 'is_featured', 'is_active')
        }),
        ('Product Details', {
            'fields': ('master', 'is_handmade', 'materials', 'dimensions', 'weight')
        }),
        ('Media', {
            'fields': ('image', 'images')
        }),
        ('Additional Info', {
            'fields': ('care_instructions', 'shipping_info')
        }),
        ('Statistics', {
            'fields': ('views_count', 'likes_count', 'orders_count')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(ProductRating)
class ProductRatingAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'rating', 'is_verified_purchase', 'created_at']
    list_filter = ['rating', 'is_verified_purchase', 'created_at']
    search_fields = ['user__username', 'product__name', 'review']
    ordering = ['-created_at']


@admin.register(ProductLike)
class ProductLikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'product__name']
    ordering = ['-created_at']


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_price', 'total_items', 'created_at']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'product', 'quantity', 'subtotal', 'created_at']
    list_filter = ['quantity', 'created_at']
    search_fields = ['cart__user__username', 'product__name']
    ordering = ['-created_at']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'user', 'customer_name', 'status', 'payment_method',
                   'is_paid', 'total_amount', 'created_at']
    list_filter = ['status', 'payment_method', 'is_paid', 'created_at']
    search_fields = ['order_number', 'customer_name', 'customer_phone', 'user__username']
    ordering = ['-created_at']
    readonly_fields = ['order_number', 'subtotal', 'delivery_fee', 'total_amount', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Order Info', {
            'fields': ('order_number', 'user', 'status')
        }),
        ('Customer Info', {
            'fields': ('customer_name', 'customer_phone', 'customer_email', 'region', 'address')
        }),
        ('Payment', {
            'fields': ('payment_method', 'payment_provider', 'is_paid')
        }),
        ('Order Details', {
            'fields': ('subtotal', 'delivery_fee', 'total_amount', 'notes')
        }),
        ('Shipping', {
            'fields': ('tracking_number', 'estimated_delivery')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product_name', 'quantity', 'subtotal']
    list_filter = ['quantity']
    search_fields = ['order__order_number', 'product_name']
    ordering = ['-order__created_at']


@admin.register(DeliveryFee)
class DeliveryFeeAdmin(admin.ModelAdmin):
    list_display = ['region', 'fee', 'free_delivery_threshold', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['region']
    ordering = ['region']


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'product__name']
    ordering = ['-created_at']
