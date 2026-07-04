from django.contrib import admin
from .models import Team, JoinRequest, TeamMembership
# Register your models here.
admin.site.register(Team)
admin.site.register(TeamMembership)
admin.site.register(JoinRequest)