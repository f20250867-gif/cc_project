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
            team=self.object,    # self.object is the saved team
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
        new_request = JoinRequest(team=team, user=request.user)
        new_request.save()
        messages.success(request, "Join request sent successfully!")
        return redirect('team-detail', pk=pk)

def view_join_requests(request, pk):
    team = get_object_or_404(Team,pk=pk)

    if not TeamMembership.objects.filter(team=team, user=request.user, role='owner').exists():
        messages.warning(request, 'you are not allowed to view this page')

    join_requests = JoinRequest.objects.filter(team=team, status='pending')

    return render(request, 'teams/join_request.html',{
        'team' : team,
        'join_requests' : join_requests
    })
