from django.urls import path
from . import views
from .views import TeamCreateView, TeamDetailView

urlpatterns = [
    path('', views.home, name='team-home'),
    path('team/new/', TeamCreateView.as_view(), name='team-create'),
    path('team/<int:pk>/',TeamDetailView.as_view(), name='team-detail'),
    path(
        'team/<int:pk>/join/',
         views.request_to_join_team, 
         name='team-join-request'
         ),
    path(
        'team/<int:pk>/invite/',
         views.invite_to_join_team_page, 
         name='invite-to-join-team-page'
         ),
    path(
        'team/<int:pk>/invite/send',
         views.invite_to_join_team, 
         name='invite-to-join-team'
         ),
    path(
        'team/<int:pk>/requests/',
         views.view_join_requests, 
         name='team-pending-requests'
         ),
    path(
        'team/<int:team_pk>/confirm_request/<int:request_pk>/',
         views.accept_join_request,
         name='accept-pending-requests'
         ),
    path(
        'team/<int:pk>/reject_request/<int:request_pk>/',
         views.reject_join_request, 
         name='reject-pending-requests'
         ),
    path(
        'team/invitations/',
         views.view_invite_request, 
         name='team-invite-requests'
         ),
    path(
        'team/confirm_invitation/<int:request_pk>/',
         views.accept_invite_request,
         name='accept-pending-invites'
         ),
    path(
        'team/reject_invitation/<int:request_pk>/',
         views.reject_invite_request, 
         name='reject-pending-invites'
         ),
    path('team/<int:pk>/members/',views.view_team_members, name='view-team-members'),
]