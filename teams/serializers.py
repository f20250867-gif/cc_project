from rest_framework import serializers
from .models import Team, JoinRequest, TeamMembership

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ('title', 'members')



