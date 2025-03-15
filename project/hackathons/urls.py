from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='hackathons/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='hackathons/logout.html'), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Hackathon URLs
    path('hackathons/', views.HackathonListView.as_view(), name='hackathon-list'),
    path('hackathons/<int:pk>/', views.HackathonDetailView.as_view(), name='hackathon-detail'),
    path('hackathons/<int:pk>/register/', views.register_hackathon, name='register-hackathon'),
    path('hackathons/<int:pk>/results/', views.HackathonResultsView.as_view(), name='hackathon-results'),
    
    # Team URLs
    path('teams/<int:team_id>/', views.team_detail, name='team-detail'),
    path('teams/<int:team_id>/submit/', views.submit_project, name='submit-project'),
]