from django.contrib import admin
from .models import Hackathon, Team, Participant, Submission, Announcement

@admin.register(Hackathon)
class HackathonAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'end_date', 'registration_deadline', 'status')
    list_filter = ('status', 'start_date')
    search_fields = ('title', 'description')

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'hackathon', 'created_at')
    list_filter = ('hackathon',)
    search_fields = ('name', 'project_name')

@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('user', 'team', 'role')
    list_filter = ('team__hackathon', 'role')
    search_fields = ('user__username', 'user__email')

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('team', 'hackathon', 'submitted_at', 'score')
    list_filter = ('hackathon', 'submitted_at')
    search_fields = ('team__name', 'project_name')

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'hackathon', 'created_at')
    list_filter = ('hackathon', 'created_at')
    search_fields = ('title', 'content')