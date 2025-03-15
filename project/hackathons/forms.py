from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Hackathon, Team, Participant, Submission

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

class HackathonRegistrationForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'project_name', 'project_description']
        
    def __init__(self, *args, **kwargs):
        self.hackathon = kwargs.pop('hackathon', None)
        super().__init__(*args, **kwargs)
        
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.hackathon = self.hackathon
        if commit:
            instance.save()
        return instance

class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ['college_id', 'department', 'year_of_study', 'skills']

class TeamMemberForm(forms.Form):
    email = forms.EmailField(label="Team Member's Email")

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['project_name', 'description', 'github_link', 'demo_link', 'presentation']
        
    def __init__(self, *args, **kwargs):
        self.team = kwargs.pop('team', None)
        self.hackathon = kwargs.pop('hackathon', None)
        super().__init__(*args, **kwargs)
        
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.team = self.team
        instance.hackathon = self.hackathon
        if commit:
            instance.save()
        return instance