from .models import TeamMembership
from tasks.models import Task


def is_team_owner(user, team):
    return TeamMembership.objects.filter(team=team, user=user, role='owner').exists()
def is_team_maintainer(user, team):
    return TeamMembership.objects.filter(team=team, user=user, role='maintainer').exists()
def is_team_member(user, team):
    return TeamMembership.objects.filter(team=team, user=user, role='member').exists()
def is_team_viewer(user, team):
    return TeamMembership.objects.filter(team=team, user=user, role='viewer').exists()
def is_present_in_team(user, team):
    return TeamMembership.objects.filter(team=team, user=user).exists()
def is_task_assigned_to(user, id):
    return Task.objects.filter(id=id, assigned_to=user).exists()
