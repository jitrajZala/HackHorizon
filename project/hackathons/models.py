from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Hackathon(models.Model):
    STATUS_CHOICES = (
        ('upcoming', 'Upcoming'),
        ('active', 'Active'),
        ('completed', 'Completed'),
    )
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    rules = models.TextField()
    prizes = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    registration_deadline = models.DateTimeField()
    max_team_size = models.PositiveIntegerField(default=4)
    image = models.ImageField(upload_to='hackathon_images/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='upcoming')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        # Auto-update status based on dates
        now = timezone.now()
        if now < self.start_date:
            self.status = 'upcoming'
        elif now >= self.start_date and now <= self.end_date:
            self.status = 'active'
        else:
            self.status = 'completed'
        super().save(*args, **kwargs)

class Team(models.Model):
    name = models.CharField(max_length=100)
    hackathon = models.ForeignKey(Hackathon, on_delete=models.CASCADE, related_name='teams')
    project_name = models.CharField(max_length=200, blank=True, null=True)
    project_description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.hackathon.title}"

class Participant(models.Model):
    ROLE_CHOICES = (
        ('leader', 'Team Leader'),
        ('member', 'Team Member'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='members')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='member')
    college_id = models.CharField(max_length=50)
    department = models.CharField(max_length=100)
    year_of_study = models.PositiveIntegerField()
    skills = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.team.name}"

class Submission(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='submissions')
    hackathon = models.ForeignKey(Hackathon, on_delete=models.CASCADE)
    project_name = models.CharField(max_length=200)
    description = models.TextField()
    github_link = models.URLField()
    demo_link = models.URLField(blank=True, null=True)
    presentation = models.FileField(upload_to='presentations/', blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    score = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    feedback = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.project_name} - {self.team.name}"

class Announcement(models.Model):
    hackathon = models.ForeignKey(Hackathon, on_delete=models.CASCADE, related_name='announcements')
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created_at']