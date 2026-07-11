from django.shortcuts import get_object_or_404, render, redirect
from projects.models import Project
from django.views.generic import (

    CreateView, 
    UpdateView, 
    DeleteView,
    DetailView
    )
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from teams.models import Team, TeamMembership
from django.contrib.auth.decorators import login_required
from teams.utils import is_team_owner,is_team_maintainer
from django.contrib import messages




class ProjectCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):

    model = Project
    fields = ['title', 'description']

    def get_team(self):
        team_id = self.kwargs.get('team_pk')
        team =  get_object_or_404(Team, id=team_id)
        return team

    def form_valid(self,form):
        form.instance.created_by = self.request.user
        form.instance.team = self.get_team()
        return super().form_valid(form)
    
    def handle_no_permission(self): 
        messages.warning(self.request, "You don't have permission to create a project!")
        return redirect('team-detail', self.kwargs.get('team_pk'))

    def test_func(self):
        team = self.get_team()
        if is_team_owner(self.request.user, team) or is_team_maintainer(self.request.user, team):
            return True
        else:
            return False


class ProjectUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Project
    fields = ['title', 'description']

    def get_team(self):
        team_id = self.kwargs.get('team_pk')
        team =  get_object_or_404(Team, id=team_id)
        return team

    def form_valid(self,form):
        form.instance.created_by = self.request.user
        form.instance.team = self.get_team()
        return super().form_valid(form)
    
    def handle_no_permission(self): 
        messages.warning(self.request, "You don't have permission to Edit a project!")
        return redirect('team-detail', self.kwargs.get('team_pk'))

    def test_func(self):
        team = self.get_team()
        if is_team_owner(self.request.user, team) or is_team_maintainer(self.request.user, team):
            return True
        else:
            return False
        


class ProjectDetailView(DetailView):
    model = Project
    
class ProjectDeleteView(LoginRequiredMixin, UserPassesTestMixin,  DeleteView):
    model = Project

    def get_success_url(self):
        return reverse_lazy('team-detail', kwargs={'pk': self.get_team().id})

    def get_team(self):
        team_id = self.kwargs.get('team_pk')
        team =  get_object_or_404(Team, id=team_id)
        return team
    
    def handle_no_permission(self): 
        messages.warning(self.request, "You don't have permission to Edit a project!")
        return redirect('team-detail', self.kwargs.get('team_pk'))

    def test_func(self):
        team = self.get_team()
        if is_team_owner(self.request.user, team) or is_team_maintainer(self.request.user, team):
            return True
        else:
            return False


