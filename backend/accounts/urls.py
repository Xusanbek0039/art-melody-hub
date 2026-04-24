from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('user/', views.UserDetailView.as_view(), name='user-detail'),
    path('achievements/', views.AchievementListCreateView.as_view(), name='achievement-list'),
    path('achievements/<int:pk>/', views.AchievementDetailView.as_view(), name='achievement-detail'),
    path('competitions/', views.CompetitionParticipationListCreateView.as_view(), name='competition-list'),
    path('competitions/<int:pk>/', views.CompetitionParticipationDetailView.as_view(), name='competition-detail'),
    path('stats/', views.user_stats, name='user-stats'),
]
