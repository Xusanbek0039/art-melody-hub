from django.urls import path
from . import views

urlpatterns = [
    path('categories/', views.InstrumentCategoryListCreateView.as_view(), name='category-list'),
    path('categories/<int:pk>/', views.InstrumentCategoryDetailView.as_view(), name='category-detail'),
    path('masters/', views.MasterListCreateView.as_view(), name='master-list'),
    path('masters/<int:pk>/', views.MasterDetailView.as_view(), name='master-detail'),
    path('masters/<int:pk>/review/', views.review_master, name='review-master'),
    path('works/', views.MasterWorkListCreateView.as_view(), name='work-list'),
    path('works/<int:pk>/', views.MasterWorkDetailView.as_view(), name='work-detail'),
    path('accessories/', views.InstrumentAccessoryListCreateView.as_view(), name='accessory-list'),
    path('accessories/<int:pk>/', views.InstrumentAccessoryDetailView.as_view(), name='accessory-detail'),
    path('repairs/', views.RepairServiceListCreateView.as_view(), name='repair-list'),
    path('repairs/<int:pk>/', views.RepairServiceDetailView.as_view(), name='repair-detail'),
    path('consultations/', views.ConsultationListCreateView.as_view(), name='consultation-list'),
    path('consultations/<int:pk>/', views.ConsultationDetailView.as_view(), name='consultation-detail'),
    path('stats/', views.masters_stats, name='masters-stats'),
]
