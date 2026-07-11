from django.db import models
from teams.models import Team
from projects.models import Project
from django.contrib.auth.models import User
from django.urls import reverse

class Task(models.Model):
    STATUS_CHOICES = [
        ('to_do', 'To Do'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]

    PRIORITY_CHOICES = [
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low'),       
    ]

    title = models.CharField(max_length=50)
    description = models.TextField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_task')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='to_do')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    assigned_to = models.ManyToManyField(User,blank=True , related_name='assigned_task')

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('project-detail', kwargs={'project_pk': self.project.pk , 'team_pk':self.project.team.pk })
    

class Comment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_comment')
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

    def __str__(self):
        return self.author
    
    def get_absolute_url(self):
        return reverse('task-detail', kwargs={'project_pk': self.task.project.pk , 'team_pk':self.task.project.team.pk , 'task_pk':self.task.pk})