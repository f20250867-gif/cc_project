from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class Team(models.Model):
    title = models.CharField(max_length=50)
    members = models.ManyToManyField(User, through='TeamMembership', related_name='teams', blank=True) 

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('team-home')
    

class TeamMembership(models.Model):
    ROLE_CHOICES = [
        ('owner', 'Owner'),
        ('maintainer', 'Maintainer'),
        ('member', 'Member'),
        ('viewer', 'Viewer'),
    ]

    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=15, choices=ROLE_CHOICES, default='viewer')
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('team', 'user')  

    def __str__(self):
        return f"{self.user.username} - {self.role}"
    
    
class JoinRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)    
