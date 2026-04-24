from django.urls import path
from . import views

urlpatterns = [
    path('', views.CompetitionListCreateView.as_view(), name='competition-list'),
    path('<int:pk>/', views.CompetitionDetailView.as_view(), name='competition-detail'),
    path('categories/', views.CompetitionCategoryListCreateView.as_view(), name='category-list'),
    path('categories/<int:pk>/', views.CompetitionCategoryDetailView.as_view(), name='category-detail'),
    path('registrations/', views.RegistrationListCreateView.as_view(), name='registration-list'),
    path('registrations/<int:pk>/', views.RegistrationDetailView.as_view(), name='registration-detail'),
    path('my-registrations/', views.UserRegistrationListView.as_view(), name='user-registrations'),
    path('register/<int:competition_id>/<int:category_id>/', views.submit_registration, name='submit-registration'),
    path('results/', views.ResultListCreateView.as_view(), name='result-list'),
    path('results/<int:pk>/', views.ResultDetailView.as_view(), name='result-detail'),
    path('judges/', views.JudgeListCreateView.as_view(), name='judge-list'),
    path('judges/<int:pk>/', views.JudgeDetailView.as_view(), name='judge-detail'),
    path('schedule/', views.ScheduleListCreateView.as_view(), name='schedule-list'),
    path('schedule/<int:pk>/', views.ScheduleDetailView.as_view(), name='schedule-detail'),
    path('news/', views.NewsListCreateView.as_view(), name='news-list'),
    path('news/<int:pk>/', views.NewsDetailView.as_view(), name='news-detail'),
    path('stats/', views.competitions_stats, name='competitions-stats'),
]
