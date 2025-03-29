from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('chat-history/', views.chat_history, name='chat_history'),
    path('projects/', views.projects, name='projects'),
    path('projects/<str:project_id>/', views.project_detail, name='project_detail'),
    path('custom-sql/', views.custom_sql_query, name='custom_sql_query'),
] 