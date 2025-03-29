from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
from .models import ChatHistory, Project
from .supabase_client import execute_sql

# Create your views here.

@csrf_exempt
@login_required
def chat_history(request):
    """View to handle chat history."""
    if request.method == 'GET':
        # Get chat history for the user
        chats = ChatHistory.get_user_chats(request.user.id)
        return JsonResponse({'chats': chats})
    
    elif request.method == 'POST':
        # Add new chat message
        data = json.loads(request.body)
        message = data.get('message')
        response = data.get('response')
        
        result = ChatHistory.add_message(
            user_id=request.user.id,
            message=message,
            response=response
        )
        return JsonResponse({'success': bool(result)})

@csrf_exempt
@login_required
def projects(request):
    """View to handle project operations."""
    if request.method == 'GET':
        # Get user's projects
        projects = Project.get_user_projects(request.user.id)
        return JsonResponse({'projects': projects})
    
    elif request.method == 'POST':
        # Create new project
        data = json.loads(request.body)
        title = data.get('title')
        description = data.get('description')
        
        if not title:
            return JsonResponse({'error': 'Title is required'}, status=400)
        
        result = Project.create_project(
            title=title,
            description=description,
            user_id=request.user.id
        )
        return JsonResponse({'success': bool(result), 'project': result})

@csrf_exempt
@login_required
def project_detail(request, project_id):
    """View to handle individual project operations."""
    if request.method == 'PUT':
        # Update project
        data = json.loads(request.body)
        title = data.get('title')
        description = data.get('description')
        
        result = Project.update_project(
            project_id=project_id,
            title=title,
            description=description
        )
        return JsonResponse({'success': bool(result)})
    
    elif request.method == 'DELETE':
        # Delete project
        result = Project.delete_project(project_id)
        return JsonResponse({'success': bool(result)})

@csrf_exempt
@login_required
def custom_sql_query(request):
    """View to handle custom SQL queries."""
    if request.method == 'POST':
        data = json.loads(request.body)
        query = data.get('query')
        params = data.get('params')
        
        # Execute the SQL query
        result = execute_sql(query, params)
        return JsonResponse({'result': result})

def index(request):
    """Main page view."""
    return render(request, 'core/index.html')
