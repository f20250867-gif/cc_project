from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import (

    CreateView, 
    UpdateView, 
    DeleteView,
    DetailView
    )
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from tasks.forms import TaskForm
from tasks.models import Task,Comment
from projects.models import Project
from django.contrib import messages
from teams.utils import is_team_owner,is_team_maintainer,is_team_member, is_present_in_team
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from teams.models import Team,TeamMembership
from django.contrib.auth.models import User




class TaskCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):

    model = Task
    pk_url_kwarg = 'task_pk'
    form_class = TaskForm

    def get_project(self):
        project_id = self.kwargs.get('project_pk')
        project =  get_object_or_404(Project, id=project_id)
        return project
    
    def get_team(self):
        return get_object_or_404(Team, pk=self.kwargs.get('team_pk'))

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        team = self.get_team()
        # setting qeuryset of assigned_to field to only include team members
        form.fields['assigned_to'].queryset = team.members.all()
        return form

    def form_valid(self,form):
        form.instance.created_by = self.request.user
        form.instance.project = self.get_project()
        return super().form_valid(form)
    
    def handle_no_permission(self): 
        messages.warning(self.request, "You don't have permission to create a task!")
        return redirect('project-detail', self.kwargs.get('projct_pk'), self.kwargs.get('team_pk'))

    def test_func(self):
        project = self.get_project()
        if is_team_owner(self.request.user, project.team) or is_team_member(self.request.user, project.team) or is_team_maintainer(self.request.user, project.team):
            return True
        else:
            return False
        

class TaskDetailView(DetailView):
    model = Task
    pk_url_kwarg = 'task_pk'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the projects
        context["comments"] = Comment.objects.filter(task=self.object)
        return context

        
class TaskUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):

    model = Task
    fields = ['title', 'description', 'priority', 'status']
    pk_url_kwarg = 'task_pk'

    def get_project(self):
        project_id = self.kwargs.get('project_pk') 
        return get_object_or_404(Project, id=project_id)
    
    def form_valid(self,form):
        form.instance.created_by = self.request.user
        form.instance.project = self.get_project()
        return super().form_valid(form)
    
    def handle_no_permission(self): 
        messages.warning(self.request, "You don't have permission to create a task!")
        return redirect('project-detail', self.kwargs.get('team_pk'), self.kwargs.get('project_pk'))

    def test_func(self):
        project = self.get_project()
        if is_team_owner(self.request.user, project.team) or is_team_member(self.request.user, project.team) or is_team_maintainer(self.request.user, project.team):
            return True 
        else:
            return False

class ProjectDeleteView(LoginRequiredMixin, UserPassesTestMixin,  DeleteView):
    model = Project
    pk_url_kwarg = 'project_pk'

    def get_success_url(self):
        return reverse_lazy('team-detail', kwargs={'pk': self.get_team().id})
    
    def get_project(self):
        project_id = self.kwargs.get('project_pk')
        project =  get_object_or_404(Project, id=project_id)
        return project
    
    def handle_no_permission(self): 
        messages.warning(self.request, "You don't have permission to create a task!")
        return redirect('project-detail', self.kwargs.get('projct_pk'), self.kwargs.get('team_pk'))

    def test_func(self):
        project = self.get_project()
        if is_team_owner(self.request.user, project.team) or is_team_maintainer(self.request.user, project.team):
            return True
        else:
            return False

@login_required
def assign_task_page(request, team_pk, project_pk, task_pk):
    task = get_object_or_404(Task, pk=task_pk)
    team = get_object_or_404(Team, pk=team_pk)
    project = task.project
    assigned_members_id = task.assigned_to.all()
    remaining_team_members = team.members.exclude(id__in=assigned_members_id)


    return render(request, 'tasks/task_assign.html',{
        'project': project,
        'remaining_team_members': remaining_team_members,
        'task': task
        
    })

@login_required
def assign_task(request, team_pk, project_pk, task_pk):

    task = get_object_or_404(Task, pk=task_pk)
    team = get_object_or_404(Team, pk=team_pk)


    if request.method != 'POST':    
        return redirect('assign-task-page', team_pk=team_pk, project_pk=project_pk, task_pk=task_pk)

    if not is_team_owner(request.user, team) or is_team_maintainer(request.user, team):
        messages.warning(request, 'you are not allowed to perform this action')
        return redirect('task-detail', team_pk=team_pk, project_pk=project_pk, task_pk=task_pk)
    
    user_id = request.POST.get('user_id')
    get_user = get_object_or_404(User, pk=user_id)

    if not user_id:
        messages.warning(request, 'Please select an correct option')
        return redirect('assign-task-page', team_pk=team_pk, project_pk=project_pk, task_pk=task_pk)

    if Task.objects.filter(assigned_to=get_user, pk=task_pk).exists():
        messages.warning(request, 'user has already been assigned same task')
        return redirect('assign-task-page', team_pk=team_pk, project_pk=project_pk, task_pk=task_pk)

    assigned_to = task.assigned_to 
    assigned_to = get_user
    assigned_to.save()

    messages.success(request, f"{get_user.username} has been assigned as a task {task.title}")
    return redirect('task-detail',task.project.team.id, task.project.id, task.id)

#to do
# def view_task_assigned(request,team_pk,project_pk,task_pk):
#     user = get_object_or_404(user=request.user)
#     team = get_object_or_404(Team, pk=team_pk)
#     task = get_object_or_404(Task, pk=task_pk)
    

#     if not is_present_in_team(user, team):
#         messages.warning(request, 'you are not allowed to perform this task!')
#         return redirect('team-home')
    
#     task_assigned = task.objects.filter(user=request.user)


class CommentCreateView(LoginRequiredMixin,CreateView):

    model = Comment
    pk_url_kwarg = 'comment_pk'
    fields = ['content']

    def get_task(self):
        task_id = self.kwargs.get('task_pk')
        task =  get_object_or_404(Task, id=task_id)
        return task

    def form_valid(self,form):
        form.instance.author = self.request.user
        form.instance.task = self.get_task()
        return super().form_valid(form)