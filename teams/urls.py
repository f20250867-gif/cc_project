from django.urls import path
from . import views
from .views import TeamCreateView, TeamDetailView,TeamListView

urlpatterns = [
    
    path('new/', TeamCreateView.as_view(), name='team-create'),
    path('<int:pk>/',TeamDetailView.as_view(), name='team-detail'),
    path(
        '<int:pk>/join/',
         views.request_to_join_team, 
         name='team-join-request'
         ),
    path(
        '<int:pk>/invite/',
         views.invite_to_join_team_page, 
         name='invite-to-join-team-page'
         ),
    path(
        '<int:pk>/invite/send',
         views.invite_to_join_team, 
         name='invite-to-join-team'
         ),
    path(
        '<int:pk>/requests/',
         views.view_join_requests, 
         name='team-pending-requests'
         ),
    path(
        '<int:team_pk>/confirm_request/<int:request_pk>/',
         views.accept_join_request,
         name='accept-pending-requests'
         ),
    path(
        '<int:team_pk>/reject_request/<int:request_pk>/',
         views.reject_join_request, 
         name='reject-pending-requests'
         ),
    path(
        'invitations/',
         views.view_invite_request, 
         name='team-invite-requests'
         ),
    path(
        'confirm_invitation/<int:request_pk>/',
         views.accept_invite_request,
         name='accept-pending-invites'
         ),
    path(
        'reject_invitation/<int:request_pk>/',
         views.reject_invite_request, 
         name='reject-pending-invites'
         ),
    path('<int:pk>/members/',views.view_team_members, name='view-team-members'),
    path('<int:pk>/assign_role/',views.assign_role_page, name='assign-role-page'),
    path('<int:pk>/assign_role/assigned',views.assign_role, name='assign-role'),
]