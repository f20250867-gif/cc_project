from multiprocessing import context

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.tasks import task

from projects.models import Project 
from .models import Team, JoinRequest, TeamMembership
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .utils import is_team_owner, is_present_in_team, is_team_maintainer
from activity.mixins import ActivityCreateUpdateLogMixin, ActivityDeleteLogMixin
from activity.models import Activity


# Create your views here.

def home(request):
    context = {
        'allteams': Team.objects.all()
    }

    return render(request, 'teams/home.html', context)

class TeamListView(ListView):
    model = Team 
    template_name = 'teams/home.html'
    context_object_name = 'allteams'
    paginate_by = 4

class TeamDetailView(LoginRequiredMixin, DetailView):
    model = Team

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the projects
        project_title = self.request.GET.get('project')
        context["projects"] = Project.objects.filter(team=self.object)
        if self.request.method == "GET":
            if project_title!=None:
                context["projects"] = Project.objects.filter(team=self.object, title__icontains=project_title)

        membership = TeamMembership.objects.filter(team=self.object, user=self.request.user).first()
        context["user_role"] = membership.role if membership else None  #retrieving all team member's role for using in template
        context["team_member"] = is_present_in_team(user=self.request.user, team=self.object) 
        return context

    

class TeamCreateView(ActivityCreateUpdateLogMixin, LoginRequiredMixin, CreateView):
    model = Team 
    fields = ['title']
    activity_action = 'created'

    def form_valid(self,form):
        form.instance.owner = self.request.user
        input =  super().form_valid(form)

        TeamMembership.objects.create(
            team=self.object,    
            user=self.request.user,
            role='owner'
        )

        return input    
    

# user sending request to join team  
@login_required
def request_to_join_team(request, pk):
    team = get_object_or_404(Team, pk=pk)

    if TeamMembership.objects.filter(team=team, user=request.user).exists():
        messages.info(request, "You are already a member of this team!")
        return redirect('team-detail', pk=pk)
    
    if JoinRequest.objects.filter(team=team, user=request.user, status='pending', initiated_by='user').exists():
        messages.info(request, "Your join request is already pending!")
        return redirect('team-detail', pk=pk)
    
    if request.method == 'POST':
        new_request = JoinRequest(team=team, user=request.user, initiated_by='user')
        new_request.save()
        messages.success(request, "Join request sent successfully!")
        return redirect('team-detail', pk=pk)

#team owner viewing request sent by users
@login_required
def view_join_requests(request, pk):
    team = get_object_or_404(Team,pk=pk)

    if not is_team_owner(request.user, team):
        messages.error(request, 'Page not found')
        return redirect('team-detail', pk=pk)

    join_requests = JoinRequest.objects.filter(team=team, status='pending', initiated_by='user')

    return render(request, 'teams/join_request.html',{
        'team' : team,
        'join_requests' : join_requests
    })
# team owner accepting request
@login_required
def accept_join_request(request, team_pk, request_pk):
    team = get_object_or_404(Team, pk=team_pk)
    join_request = get_object_or_404(JoinRequest, pk=request_pk)
    user = join_request.user

    if not is_team_owner(request.user, team):
        messages.error(request, 'you are not allowed to perform this action')
        return redirect('team-detail', pk=team_pk)

    join_request.status = 'accepted'
    join_request.save()

    # handling duplicate request
    if JoinRequest.objects.filter(team=team, status='pending', user=request.user, initiated_by='owner').exists():
        dublicate_join_request =  JoinRequest.objects.filter(user = request.user, team=team, status='pending', initiated_by='owner').first()
        dublicate_join_request.status = 'accepted'
        dublicate_join_request.save()

    # adding member to team and saving actitvity
    TeamMembership.objects.create(team=team,user=join_request.user,role='member')
    Activity.objects.create(target=team,action='joined',user=join_request.user)

    messages.success(request, f"{join_request.user.username} has been added to the team.")
    return redirect('team-pending-requests', pk=team_pk)

#team owner rejecting request
@login_required
def reject_join_request(request, team_pk, request_pk):
    team = get_object_or_404(Team, pk=team_pk)
    join_request = get_object_or_404(JoinRequest, pk=request_pk)

    if not is_team_owner(request.user, team):
        messages.error(request, 'you are not allowed to perform this action')
        return redirect('team-detail', pk=team_pk)

    join_request.status = 'rejected'
    join_request.save()

    messages.info(request, f"{join_request.user.username} 's join request has been rejected.")
    return redirect('team-pending-requests', pk=team_pk)

#owner sending request page
@login_required
def invite_to_join_team_page(request, pk):

    team = get_object_or_404(Team, pk=pk)

    if not is_team_owner(request.user, team) or is_team_maintainer(request.user, team):
        messages.error(request, 'you are not allowed to perform this action')
        return redirect('team-detail', pk=pk)
    
    existing_members = Team.objects.all()
    remaining_users = User.objects.exclude(id__in=existing_members)
    return render(request, 'teams/send_invite_request.html',{
        'team': team,
        'remaining_users': remaining_users
    })

#owner sending invite view
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

    if not is_team_owner(request.user, team) or is_team_maintainer(request.user, team):
        messages.error(request, 'you are not allowed to perform this action')
        return redirect('team-detail', pk=pk)
    
    if JoinRequest.objects.filter(team=team, user=user, status='pending', initiated_by='owner').exists():
        messages.info(request, "join invitation is already pending")
        return redirect('invite-to-join-team-page', pk=pk)
    
    if TeamMembership.objects.filter(team=team, user=user).exists():
        messages.warning(request, "User is already a member of this team!")
        return redirect('invite-to-join-team-page', pk=pk)

    JoinRequest.objects.create(team=team, user=user, initiated_by='owner') 
    messages.success(request, "Join invitation sent successfully!")
    return redirect('team-detail', pk=pk)
    
#page for user to view all invitations from teams
@login_required
def view_invite_request(request):
    invite_requests = JoinRequest.objects.filter(user = request.user ,status='pending', initiated_by='owner')

    return render(request, 'teams/team_invite_request.html',{
        'invite_requests' : invite_requests
    })

#user accepting team request
@login_required
def accept_invite_request(request, request_pk):
    invite_request = get_object_or_404(JoinRequest, pk=request_pk)
    team = invite_request.team

    invite_request.status = 'accepted'
    invite_request.save()
    Activity.objects.create(target=team,action='joined',user=invite_request.user)
    TeamMembership.objects.create(team=team,user=invite_request.user,role='member')

    messages.success(request, f"You have successfully joined the team {team.title}.")
    return redirect('team-detail', pk=team.pk)

#user rejecting team request
@login_required
def reject_invite_request(request,request_pk):
    invite_request = get_object_or_404(JoinRequest, pk=request_pk)
    team = invite_request.team

    invite_request.status = 'rejected'
    invite_request.save()

    messages.warning(request, f"You have successfully rejected the team invite of {team.title}.")
    return redirect('team-detail', pk=team.pk)

# view team members page
def view_team_members(request, pk):
    team = get_object_or_404(Team, pk=pk)
    members = TeamMembership.objects.filter(team=team)

    if not is_present_in_team(request.user,team):
        messages.warning(request, 'you are not allowed to perform this action')
        return redirect('team-detail', pk=pk)

    return render(request, 'teams/team_members.html', {
        'team': team,
        'members': members  
    })

@login_required
def assign_role_page(request, pk):
    team = get_object_or_404(Team, pk=pk)
    existing_members_id = team.members.all()
    existing_users = team.members.filter(id__in=existing_members_id).exclude(membership__role='owner').distinct()

    if not is_team_owner(user=request.user,team=team):
        messages.error(request, 'Page not found')
        return redirect('team-detail', pk=pk)
    
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

    if not is_team_owner(user=request.user,team=team):
        messages.error(request, 'you are not allowed to perform this action')
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
    # Activity.objects.create(target=TeamMembership,action='was assigned',user=get_user)
    messages.success(request, f"{get_user.username} has been assigned as a {team_membership.role}.")
    return redirect('view-team-members', pk=pk)




