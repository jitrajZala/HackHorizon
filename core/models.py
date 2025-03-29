from django.db import models
from django.contrib.auth.models import User
from .supabase_client import get_supabase_client, get_table_data, insert_data, update_data, delete_data
from datetime import datetime

class SupabaseModel:
    """Base class for models that interact with Supabase."""
    table_name = None  # Override in subclass

    @classmethod
    def get_all(cls):
        """Get all records from the table."""
        return get_table_data(cls.table_name)

    @classmethod
    def create(cls, data):
        """Create a new record."""
        return insert_data(cls.table_name, data)

    @classmethod
    def update(cls, data, match_criteria):
        """Update existing records."""
        return update_data(cls.table_name, data, match_criteria)

    @classmethod
    def delete(cls, match_criteria):
        """Delete records."""
        return delete_data(cls.table_name, match_criteria)

class ChatHistory(SupabaseModel):
    """Model for chat history table in Supabase."""
    table_name = 'chat_history'

    @classmethod
    def get_user_chats(cls, user_id):
        """Get chat history for a specific user."""
        client = get_supabase_client()
        try:
            result = client.table(cls.table_name)\
                .select("*")\
                .eq('user_id', user_id)\
                .order('timestamp', desc=True)\
                .execute()
            return result.data
        except Exception as e:
            print(f"Error fetching user chats: {e}")
            return None

    @classmethod
    def add_message(cls, user_id, message, response, timestamp=None):
        """Add a new chat message."""
        data = {
            'user_id': user_id,
            'message': message,
            'response': response,
            'timestamp': timestamp
        }
        return cls.create(data)

class Project(SupabaseModel):
    """Model for projects table in Supabase."""
    table_name = 'projects'

    @classmethod
    def get_user_projects(cls, user_id):
        """Get projects for a specific user."""
        client = get_supabase_client()
        try:
            result = client.table(cls.table_name)\
                .select("*")\
                .eq('user_id', user_id)\
                .order('created_at', desc=True)\
                .execute()
            return result.data
        except Exception as e:
            print(f"Error fetching user projects: {e}")
            return None

    @classmethod
    def create_project(cls, title, description, user_id):
        """Create a new project."""
        data = {
            'title': title,
            'description': description,
            'user_id': user_id,
            'created_at': datetime.now().isoformat()
        }
        return cls.create(data)

    @classmethod
    def update_project(cls, project_id, title=None, description=None):
        """Update an existing project."""
        data = {}
        if title is not None:
            data['title'] = title
        if description is not None:
            data['description'] = description
        
        if data:
            return cls.update(data, {'id': project_id})
        return None

    @classmethod
    def delete_project(cls, project_id):
        """Delete a project."""
        return cls.delete({'id': project_id})

class UserProfile(models.Model):
    """User profile model stored in Django's database."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profile for {self.user.username}"

class Hackathon(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    registration_deadline = models.DateTimeField()
    max_team_size = models.IntegerField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

class HackathonRegistration(models.Model):
    hackathon = models.ForeignKey(Hackathon, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    team_name = models.CharField(max_length=100)
    registered_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('hackathon', 'user')

class Challenge(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES)
    points = models.IntegerField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

class ChallengeSubmission(models.Model):
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    solution = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_correct = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('challenge', 'user')
