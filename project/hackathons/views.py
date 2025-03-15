from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.db.models import Q
from django.contrib.auth.models import User

from .models import Hackathon, Team, Participant, Submission, Announcement
from .forms import UserRegisterForm, HackathonRegistrationForm, ParticipantForm, TeamMemberForm, SubmissionForm

def home(request):
    upcoming_hackathons = Hackathon.objects.filter(status='upcoming').order_by('start_date')[:3]
    active_hackathons = Hackathon.objects.filter(status='active').order_by('end_date')[:3]
    recent_hackathons = Hackathon.objects.filter(status='completed').order_by('-end_date')[:3]
    
    context = {
        'upcoming_hackathons': upcoming_hackathons,
        'active_hackathons': active_hackathons,
        'recent_hackathons': recent_hackathons,
    }
    return render(request, 'hackathons/home.html', context)

def about(request):
    return render(request, 'hackathons/about.html', {'title': 'About'})

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'hackathons/register.html', {'form': form})

class HackathonListView(ListView):
    model = Hackathon
    template_name = 'hackathons/hackathon_list.html'
    context_object_name = 'hackathons'
    ordering = ['-start_date']
    paginate_by = 6
    
    def get_queryset(self):
        query = self.request.GET.get('q')
        status_filter = self.request.GET.get('status')
        
        queryset = Hackathon.objects.all()
        
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | 
                Q(description__icontains=query)
            )
        
        if status_filter and status_filter != 'all':
            queryset = queryset.filter(status=status_filter)
            
        return queryset.order_by('-start_date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_filter'] = self.request.GET.get('status', 'all')
        context['search_query'] = self.request.GET.get('q', '')
        return context

class HackathonDetailView(DetailView):
    model = Hackathon
    template_name = 'hackathons/hackathon_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        hackathon = self.get_object()
        
        # Check if user is already registered
        user_registered = False
        user_team = None
        
        if self.request.user.is_authenticated:
            participants = Participant.objects.filter(user=self.request.user, team__hackathon=hackathon)
            if participants.exists():
                user_registered = True
                user_team = participants.first().team
        
        context['user_registered'] = user_registered
        context['user_team'] = user_team
        context['announcements'] = hackathon.announcements.all()[:5]
        
        # Registration status
        now = timezone.now()
        context['registration_open'] = now <= hackathon.registration_deadline
        context['hackathon_started'] = now >= hackathon.start_date
        context['hackathon_ended'] = now > hackathon.end_date
        
        return context

@login_required
def register_hackathon(request, pk):
    hackathon = get_object_or_404(Hackathon, pk=pk)
    
    # Check if registration is still open
    if timezone.now() > hackathon.registration_deadline:
        messages.error(request, 'Registration for this hackathon has closed.')
        return redirect('hackathon-detail', pk=hackathon.pk)
    
    # Check if user is already registered
    if Participant.objects.filter(user=request.user, team__hackathon=hackathon).exists():
        messages.warning(request, 'You are already registered for this hackathon.')
        return redirect('hackathon-detail', pk=hackathon.pk)
    
    if request.method == 'POST':
        team_form = HackathonRegistrationForm(request.POST, hackathon=hackathon)
        participant_form = ParticipantForm(request.POST)
        
        if team_form.is_valid() and participant_form.is_valid():
            team = team_form.save()
            
            # Create participant (team leader)
            participant = participant_form.save(commit=False)
            participant.user = request.user
            participant.team = team
            participant.role = 'leader'
            participant.save()
            
            messages.success(request, f'You have successfully registered for {hackathon.title}!')
            return redirect('team-detail', team_id=team.id)
    else:
        team_form = HackathonRegistrationForm(hackathon=hackathon)
        participant_form = ParticipantForm()
    
    return render(request, 'hackathons/register_hackathon.html', {
        'hackathon': hackathon,
        'team_form': team_form,
        'participant_form': participant_form
    })

@login_required
def team_detail(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    hackathon = team.hackathon
    
    # Check if user is part of the team
    try:
        participant = Participant.objects.get(user=request.user, team=team)
        is_leader = participant.role == 'leader'
    except Participant.DoesNotExist:
        messages.error(request, 'You are not a member of this team.')
        return redirect('hackathon-detail', pk=hackathon.pk)
    
    # Handle adding team members
    if request.method == 'POST' and is_leader:
        form = TeamMemberForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            
            try:
                user = User.objects.get(email=email)
                
                # Check if team is full
                if team.members.count() >= hackathon.max_team_size:
                    messages.error(request, f'Your team has reached the maximum size of {hackathon.max_team_size}.')
                # Check if user is already in a team for this hackathon
                elif Participant.objects.filter(user=user, team__hackathon=hackathon).exists():
                    messages.error(request, f'User {user.username} is already registered for this hackathon.')
                else:
                    # Add user to team
                    Participant.objects.create(
                        user=user,
                        team=team,
                        role='member',
                        college_id='',  # These fields will need to be updated by the member
                        department='',
                        year_of_study=1
                    )
                    messages.success(request, f'{user.username} has been added to your team.')
            except User.DoesNotExist:
                messages.error(request, f'No user found with email {email}.')
            
            return redirect('team-detail', team_id=team.id)
    else:
        form = TeamMemberForm()
    
    # Get team submissions
    submissions = Submission.objects.filter(team=team).order_by('-submitted_at')
    
    context = {
        'team': team,
        'hackathon': hackathon,
        'members': team.members.all(),
        'is_leader': is_leader,
        'form': form,
        'submissions': submissions,
        'can_submit': hackathon.status == 'active'
    }
    
    return render(request, 'hackathons/team_detail.html', context)

@login_required
def submit_project(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    hackathon = team.hackathon
    
    # Check if user is part of the team
    if not Participant.objects.filter(user=request.user, team=team).exists():
        messages.error(request, 'You are not a member of this team.')
        return redirect('hackathon-detail', pk=hackathon.pk)
    
    # Check if hackathon is active
    if hackathon.status != 'active':
        messages.error(request, 'Submissions are only allowed during the active phase of the hackathon.')
        return redirect('team-detail', team_id=team.id)
    
    if request.method == 'POST':
        form = SubmissionForm(request.POST, request.FILES, team=team, hackathon=hackathon)
        if form.is_valid():
            submission = form.save()
            messages.success(request, 'Your project has been submitted successfully!')
            return redirect('team-detail', team_id=team.id)
    else:
        # Pre-fill with existing submission if any
        try:
            submission = Submission.objects.filter(team=team).latest('submitted_at')
            form = SubmissionForm(instance=submission, team=team, hackathon=hackathon)
        except Submission.DoesNotExist:
            form = SubmissionForm(initial={'project_name': team.project_name}, team=team, hackathon=hackathon)
    
    return render(request, 'hackathons/submit_project.html', {
        'form': form,
        'team': team,
        'hackathon': hackathon
    })

class HackathonResultsView(DetailView):
    model = Hackathon
    template_name = 'hackathons/hackathon_results.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        hackathon = self.get_object()
        
        # Only show results for completed hackathons
        if hackathon.status != 'completed':
            context['results_available'] = False
            return context
        
        # Get top submissions
        top_submissions = Submission.objects.filter(
            hackathon=hackathon,
            score__isnull=False
        ).order_by('-score')[:10]
        
        context['results_available'] = True
        context['top_submissions'] = top_submissions
        return context

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    # Get user's teams
    user_teams = Team.objects.filter(members__user=request.user).order_by('-created_at')
    
    # Get hackathons the user is participating in
    participating_hackathons = Hackathon.objects.filter(
        teams__members__user=request.user
    ).distinct()
    
    # Get upcoming hackathons
    upcoming_hackathons = Hackathon.objects.filter(
        status='upcoming'
    ).exclude(
        teams__members__user=request.user
    ).order_by('start_date')[:5]
    
    context = {
        'user_teams': user_teams,
        'participating_hackathons': participating_hackathons,
        'upcoming_hackathons': upcoming_hackathons,
    }
    
    return render(request, 'hackathons/dashboard.html', context)