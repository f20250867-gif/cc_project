from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User 
from .models import Team, JoinRequest, TeamMembership
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.

def home(request):
    context = {
        'allteams': Team.objects.all()
    }

    return render(request, 'teams/home.html', context)

class TeamDetailView(DetailView):
    model = Team

class TeamCreateView(LoginRequiredMixin, CreateView):
    model = Team 
    fields = ['title']

    def form_valid(self,form):
        form.instance.member = self.request.user
        input =  super().form_valid(form)

        TeamMembership.objects.create(
            team=self.object,    
            user=self.request.user,
            role='owner'
        )

        return input    
    
@login_required
def request_to_join_team(request, pk):
    team = get_object_or_404(Team, pk=pk)

    if TeamMembership.objects.filter(team=team, user=request.user).exists():
        messages.warning(request, "You are already a member of this team!")
        return redirect('team-detail', pk=pk)
    
    if JoinRequest.objects.filter(team=team, user=request.user, status='pending').exists():
        messages.info(request, "Your join request is already pending!")
        return redirect('team-detail', pk=pk)
    
    if request.method == 'POST':
        new_request = JoinRequest(team=team, user=request.user, initiated_by='user')
        new_request.save()
        messages.success(request, "Join request sent successfully!")
        return redirect('team-detail', pk=pk)

@login_required
def view_join_requests(request, pk):
    team = get_object_or_404(Team,pk=pk)

    if not TeamMembership.objects.filter(team=team, user=request.user, role='owner').exists():
        messages.warning(request, 'you are not allowed to view this page')

    join_requests = JoinRequest.objects.filter(team=team, status='pending')

    return render(request, 'teams/join_request.html',{
        'team' : team,
        'join_requests' : join_requests
    })

@login_required
def accept_join_request(request, team_pk, request_pk):
    team = get_object_or_404(Team, pk=team_pk)
    join_request = get_object_or_404(JoinRequest, pk=request_pk)

    if not TeamMembership.objects.filter(team=team, user=request.user, role='owner').exists():
        messages.warning(request, 'you are not allowed to perform this action')
        return redirect('team-detail', pk=team_pk)

    join_request.status = 'accepted'
    join_request.save()

    TeamMembership.objects.create(team=team,user=join_request.user,role='member')

    messages.success(request, f"{join_request.user.username} has been added to the team.")
    return redirect('view-join-requests', pk=team_pk)

@login_required
def reject_join_request(request, team_pk, request_pk):
    team = get_object_or_404(Team, pk=team_pk)
    join_request = get_object_or_404(JoinRequest, pk=request_pk)

    if not TeamMembership.objects.filter(team=team, user=request.user, role='owner').exists():
        messages.warning(request, 'you are not allowed to perform this action')
        return redirect('team-detail', pk=team_pk)
    
    if join_request.status != 'pending':
        messages.warning(request, 'This join request has already been processed.')
        return redirect('view-join-requests', pk=team_pk)

    join_request.status = 'rejected'
    join_request.save()

    messages.info(request, f"{join_request.user.username} 's join request has been rejected.")
    return redirect('view-join-requests', pk=team_pk)

@login_required
def invite_to_join_team(request, pk):
    team = get_object_or_404(Team, pk=pk)

    if request.method != 'POST':    
        return redirect('team-detail', pk=pk)
    user_id = request.POST.get('user_id')

    if not user_id:
        messages.warning(request, 'No user selected.')
        return redirect('team-detail', pk=pk)

    user = get_object_or_404(User, pk=user_id)

    if not TeamMembership.objects.filter(team=team, user=request.user, role='owner').exists():
        messages.warning(request, 'you are not allowed to perform this action')
        return redirect('team-detail', pk=pk)
    
    if JoinRequest.objects.filter(team=team, user=user, status='pending').exists():
        messages.info(request, "Your join request is already pending!")
        return redirect('team-detail', pk=pk)
    
    if TeamMembership.objects.filter(team=team, user=user).exists():
        messages.warning(request, "User is already a member of this team!")
        return redirect('team-detail', pk=pk)

    
    JoinRequest.objects.create(team=team, user=user, initiated_by='owner') 
    messages.success(request, "Join invitation sent successfully!")
    return redirect('team-detail', pk=pk)
    

@login_required
def view_invite_request(request,pk):
    team = get_object_or_404(Team,pk=pk)
    invite_requests = JoinRequest.objects.filter(team=team, user = request.user ,status='pending', initiated_by='owner')

    if request.user in team.members.all():
        messages.warning(request, 'you are already a member of this team')
        return redirect('team-detail', pk=pk)

    return render(request, 'teams/team_invite_request.html',{
        'team' : team,
        'invite_requests' : invite_requests
    })

@login_required
def accept_invite_request(request, team_pk, request_pk):
    team = get_object_or_404(Team, pk=team_pk)
    join_request = get_object_or_404(JoinRequest, pk=request_pk)

    if join_request.user != request.user:
        messages.warning(request, 'you are not allowed to perform this action')
        return redirect('team-detail', pk=team_pk)

    join_request.status = 'accepted'
    join_request.save()

    TeamMembership.objects.create(team=team,user=join_request.user,role='member')

    messages.success(request, f"You have successfully joined the team {team.title}.")
    return redirect('view-join-requests', pk=team_pk)

@login_required
def reject_invite_request(request, team_pk, request_pk):
    team = get_object_or_404(Team, pk=team_pk)
    join_request = get_object_or_404(JoinRequest, pk=request_pk)

    if join_request.user != request.user:
        messages.warning(request, 'you are not allowed to perform this action')
        return redirect('team-detail', pk=team_pk)

    join_request.status = 'rejected'
    join_request.save()

    messages.success(request, f"You have successfully joined the team {team.title}.")
    return redirect('view-join-requests', pk=team_pk)

def view_team_members(request, pk):
    team = get_object_or_404(Team, pk=pk)
    members = TeamMembership.objects.filter(team=team)

    is_owner = TeamMembership.objects.get(team=team,user=request.user,role='owner').exists()

    if not is_owner:
        messages.warning(request, 'you are not allowed to perform this action')
        return redirect('team-detail', pk=pk)

    return render(request, 'teams/team_members.html', {
        'team': team,
        'members': members
    })