from .models import TeamMembership


def is_team_owner(user, team):
    return TeamMembership.objects.filter(team=team, user=user, role='owner').exists()
def is_team_maintainer(user, team):
    return TeamMembership.objects.filter(team=team, user=user, role='maintainer').exists()
def is_team_member(user, team):
    return TeamMembership.objects.filter(team=team, user=user, role='member').exists()
def is_team_viewer(user, team):
    return TeamMembership.objects.filter(team=team, user=user, role='viewer').exists()