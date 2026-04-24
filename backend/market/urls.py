from django.urls import path
from . import views

urlpatterns = [
    path('categories/', views.ProductCategoryListCreateView.as_view(), name='product-category-list'),
    path('categories/<int:pk>/', views.ProductCategoryDetailView.as_view(), name='product-category-detail'),
    path('', views.ProductListCreateView.as_view(), name='product-list'),
    path('<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('<int:pk>/rate/', views.rate_product, name='rate-product'),
    path('<int:pk>/like/', views.like_product, name='like-product'),
    path('cart/', views.CartView.as_view(), name='cart'),
    path('cart/add/', views.add_to_cart, name='add-to-cart'),
    path('cart/items/<int:item_id>/', views.update_cart_item, name='update-cart-item'),
    path('cart/items/<int:item_id>/remove/', views.remove_from_cart, name='remove-from-cart'),
    path('orders/', views.OrderListCreateView.as_view(), name='order-list'),
    path('orders/create/', views.create_order, name='create-order'),
    path('orders/<int:pk>/', views.OrderDetailView.as_view(), name='order-detail'),
    path('delivery-fees/', views.DeliveryFeeListCreateView.as_view(), name='delivery-fee-list'),
    path('delivery-fees/<int:pk>/', views.DeliveryFeeDetailView.as_view(), name='delivery-fee-detail'),
    path('delivery-fee/', views.get_delivery_fee, name='get-delivery-fee'),
    path('wishlist/', views.WishlistListCreateView.as_view(), name='wishlist-list'),
    path('wishlist/<int:pk>/', views.WishlistDetailView.as_view(), name='wishlist-detail'),
    path('stats/', views.market_stats, name='market-stats'),
]
