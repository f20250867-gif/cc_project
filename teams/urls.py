from django.urls import path
from . import views
from .views import TeamCreateView, TeamDetailView

urlpatterns = [
    path('', views.home, name='team-home'),
    path('team/new/', TeamCreateView.as_view(), name='team-create'),
    path('team/<int:pk>/',TeamDetailView.as_view(), name='team-detail'),
    path('team/<int:pk>/join/',views.request_to_join_team, name='team-join-request'),
    path('team/<int:pk>/requests/',views.view_join_requests, name='team-pending-requests'),
]