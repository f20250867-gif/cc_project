from django.db import models
from teams.models import Team
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.

class Project(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('team-detail', kwargs={'pk': self.team.pk})