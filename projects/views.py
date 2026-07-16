from urllib import request
from django.contrib.messages.views import SuccessMessageMixin

from django.shortcuts import get_object_or_404, render, redirect
from projects.models import Project
from django.urls import reverse_lazy
from django.views.generic import (

    CreateView, 
    UpdateView, 
    DeleteView,
    DetailView,
    ListView,
    )
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
import tasks
from teams.models import Team, TeamMembership
from django.contrib.auth.decorators import login_required
from teams.utils import is_team_owner,is_team_maintainer,is_present_in_team
from django.contrib import messages
from tasks.models import Task
from activity.mixins import ActivityCreateUpdateLogMixin, ActivityDeleteLogMixin
from .forms import FilterTaskType



class ProjectCreateView(ActivityCreateUpdateLogMixin, LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin ,CreateView):

    model = Project
    fields = ['title', 'description']
    pk_url_kwarg = 'project_pk'
    activity_action = 'created'

    def get_team(self):
        team_id = self.kwargs.get('team_pk')
        team =  get_object_or_404(Team, id=team_id)
        return team

    def form_valid(self,form):
        form.instance.created_by = self.request.user
        form.instance.team = self.get_team()
        return super().form_valid(form)
    
    def handle_no_permission(self): 
        messages.error(self.request, "You don't have permission to create a project!")
        return redirect('team-home')

    def test_func(self):
        team = self.get_team()
        if is_team_owner(self.request.user, team) or is_team_maintainer(self.request.user, team):
            return True
        else:
            return False
        
    success_message = "'%(project_title)s'  project was created successfully"

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            project_title=self.object.title,
        )



class ProjectListView(ListView):
    model = Project 


class ProjectUpdateView(ActivityCreateUpdateLogMixin, LoginRequiredMixin, UserPassesTestMixin,SuccessMessageMixin, UpdateView):
    model = Project
    fields = ['title', 'description']
    pk_url_kwarg = 'project_pk'
    activity_action = 'updated'

    def get_team(self):
        team_id = self.kwargs.get('team_pk')
        team =  get_object_or_404(Team, id=team_id)
        return team

    def form_valid(self,form):
        form.instance.created_by = self.request.user
        form.instance.team = self.get_team()
        return super().form_valid(form)
    
    def handle_no_permission(self): 
        messages.error(self.request, "You don't have permission to Edit a project!")
        return redirect('team-home')

    def test_func(self):
        team = self.get_team()
        if is_team_owner(self.request.user, team) or is_team_maintainer(self.request.user, team):
            return True
        else:
            return False
        
    success_message = "'%(project_title)s'  project was updated successfully"

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            project_title=self.object.title,
        )

class ProjectDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Project
    pk_url_kwarg = 'project_pk'
    def get_team(self):
        team_id = self.kwargs.get('team_pk')
        team =  get_object_or_404(Team, id=team_id)
        return team

    def handle_no_permission(self): 
        messages.error(self.request, "Page not found")
        return redirect('team-home')

    def test_func(self):
        team = self.get_team()
        if is_present_in_team(self.request.user, team):
            return True
        else:
            return False

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the projects
        tasks = Task.objects.filter(project=self.object)

        # get value to be searched from user
        task_title = self.request.GET.get('task')
        status_types = self.request.GET.getlist('status_task_type')
        priority_types = self.request.GET.getlist('priority_task_type')

        # putting retrieved data from user's input in tasks
        if self.request.method=="GET":
            if task_title!=None: 
                tasks = tasks.filter(title__icontains=task_title, project=self.object)

            if status_types:
                tasks = tasks.filter(status__in=status_types, project=self.object)

            if priority_types:
                tasks = tasks.filter(priority__in=priority_types, project=self.object)
        # context for filter search
        context["form"] = FilterTaskType()
        context["tasks"] = tasks
        membership = TeamMembership.objects.filter(team=self.object.team, user=self.request.user).first()
        # context for rendering role based html file
        context["user_role"] = membership.role if membership else None
        context["team_member"] = is_present_in_team(user=self.request.user, team=self.object.team)

        return context

    # def search_task(self, request):
    #     tasks = Task.objects.all()
    #     if request.method=="GET":
    #         task_title = request.GET.get('task')
    #         if task_title !=None:
    #             tasks = Task.objects.filter(title=task_title, project=self.object)

    #     return render(request, 'projects/project_detail.html', {'tasks':tasks})

   
class ProjectDeleteView(ActivityDeleteLogMixin, LoginRequiredMixin, UserPassesTestMixin,SuccessMessageMixin, DeleteView):
    model = Project
    pk_url_kwarg = 'project_pk'
    activity_action = 'deleted'

    def get_success_url(self):
        return reverse_lazy('team-detail', kwargs={'pk': self.get_team().id})
    
    def get_team(self):
        team_id = self.kwargs.get('team_pk')
        team =  get_object_or_404(Team, id=team_id)
        return team
    
    def handle_no_permission(self): 
        messages.error(self.request, "You don't have permission to Edit a project!")
        return redirect('project-detail', self.kwargs.get('team_pk'), self.kwargs.get('project_pk'))

    def test_func(self):
        team = self.get_team()
        if is_team_owner(self.request.user, team) or is_team_maintainer(self.request.user, team):
            return True
        else:
            return False
        
    success_message = "'%(project_title)s'  project was deleted successfully"

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            project_title=self.object.title,
        )



