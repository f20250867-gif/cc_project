from multiprocessing import context

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User

from projects.models import Project 
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

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the projects
        context["projects"] = Project.objects.filter(team=self.object)
        return context

class TeamCreateView(LoginRequiredMixin, CreateView):
    model = Team 
    fields = ['title']

    def form_valid(self,form):
        form.instance.owner = self.request.user
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
    return redirect('team-detail', pk=team_pk)

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
def invite_to_join_team_page(request, pk):
    team = get_object_or_404(Team, pk=pk)
    existing_members = Team.objects.all()
    remaining_users = User.objects.exclude(id__in=existing_members)
    return render(request, 'teams/send_invite_request.html',{
        'team': team,
        'remaining_users': remaining_users
    })

@login_required
def invite_to_join_team(request, pk):
    team = get_object_or_404(Team, pk=pk)

    if request.method != 'POST':    
        return redirect('invite-to-join-team-page', pk=pk)
    
    user_id = request.POST.get('user_id')

    if not user_id:
        messages.warning(request, 'No user selected.')
        return redirect('invite-to-join-team-page', pk=pk)

    user = get_object_or_404(User, pk=user_id)

    if not TeamMembership.objects.filter(team=team, user=request.user, role='owner').exists():
        messages.warning(request, 'you are not allowed to perform this action')
        return redirect('invite-to-join-team-page', pk=pk)
    
    if JoinRequest.objects.filter(team=team, user=user, status='pending').exists():
        messages.info(request, "Your join request is already pending!")
        return redirect('invite-to-join-team-page', pk=pk)
    
    if TeamMembership.objects.filter(team=team, user=user).exists():
        messages.warning(request, "User is already a member of this team!")
        return redirect('invite-to-join-team-page', pk=pk)

    JoinRequest.objects.create(team=team, user=user, initiated_by='owner') 
    messages.success(request, "Join invitation sent successfully!")
    return redirect('team-detail', pk=pk)
    

@login_required
def view_invite_request(request):
    invite_requests = JoinRequest.objects.filter(user = request.user ,status='pending', initiated_by='owner')

    return render(request, 'teams/team_invite_request.html',{
        'invite_requests' : invite_requests
    })

@login_required
def accept_invite_request(request, request_pk):
    invite_request = get_object_or_404(JoinRequest, pk=request_pk)
    team = invite_request.team

    invite_request.status = 'accepted'
    invite_request.save()

    TeamMembership.objects.create(team=team,user=invite_request.user,role='member')

    messages.success(request, f"You have successfully joined the team {team.title}.")
    return redirect('team-detail', pk=team.pk)

@login_required
def reject_invite_request(request,request_pk):
    invite_request = get_object_or_404(JoinRequest, pk=request_pk)
    team = invite_request.team

    invite_request.status = 'rejected'
    invite_request.save()

    messages.success(request, f"You have successfully joined the team {team.title}.")
    return redirect('team-detail', pk=team.pk)

def view_team_members(request, pk):
    team = get_object_or_404(Team, pk=pk)
    members = TeamMembership.objects.filter(team=team)
    is_owner = TeamMembership.objects.filter(team=team,user=request.user,role='owner').exists()

    if not is_owner:
        messages.warning(request, 'you are not allowed to perform this action')
        return redirect('team-detail', pk=pk)

    return render(request, 'teams/team_members.html', {
        'team': team,
        'members': members
    })

@login_required
def assign_role_page(request, pk):
    team = get_object_or_404(Team, pk=pk)
    existing_members = TeamMembership.objects.filter(team=team).values_list('user_id', flat=True)
    existing_users = User.objects.filter(id__in=existing_members).exclude(membership__role='owner').distinct()

    for user in existing_users:
        if TeamMembership.role == 'owner':
            existing_users.remove(user)

    selected_roles = [
        (value, label)
        for value, label in TeamMembership.ROLE_CHOICES
        if value != 'owner'
    ]

    return render(request, 'teams/assign_role.html',{
        'team': team,
        'existing_users': existing_users,
        'roles': selected_roles
        
    })

@login_required
def assign_role(request, pk):

    team = get_object_or_404(Team, pk=pk)

    if request.method != 'POST':    
        return redirect('assign-role-page', pk=pk)

    if not TeamMembership.objects.filter(team=team, user=request.user, role='owner').exists():
        messages.warning(request, 'you are not allowed to perform this action')
        return redirect('team-detail', pk=pk)
    
    user_id = request.POST.get('user_id')
    get_role = request.POST.get('role')
    get_user = get_object_or_404(User, pk=user_id)
    team_membership = get_object_or_404(TeamMembership, team=team, user=get_user)

    if not (user_id or get_role.id):
        messages.warning(request, 'Please select an option')
        return redirect('assign-role-page', pk=pk)

    if team_membership.role == get_role:
        messages.warning(request, 'user already has the same role')
        return redirect('assign-role-page', pk=pk)
    
    valid_roles = []
    for value, label in TeamMembership.ROLE_CHOICES:
        valid_roles.append(value)
    if get_role not in valid_roles or get_role == 'owner':
        messages.warning(request, 'Invalid role selection')
        return redirect('assign-role-page', pk=pk)
    
    team_membership.role = get_role
    team_membership.save()
    messages.success(request, f"{get_user.username} has been assigned as a {team_membership.role}.")
    return redirect('view-team-members', pk=pk)




