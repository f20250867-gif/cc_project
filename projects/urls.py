from django.urls import path

from .views import ProjectCreateView,ProjectUpdateView,ProjectDetailView,ProjectDeleteView



urlpatterns = [
    # path('team/<int:pk>/project/', team_detail_project, name='team-detail-project'),
    path('team/<int:team_pk>/project/create/', ProjectCreateView.as_view(), name='project-create'),
    path('team/<int:team_pk>/project/<int:pk>/update/', ProjectUpdateView.as_view(), name='project-update'),
    path('team/<int:team_pk>/project/<int:pk>/delete/', ProjectDeleteView.as_view(), name='project-delete'),
    path('team/<int:team_pk>/project/<int:pk>/', ProjectDetailView.as_view(), name='project-detail'),
]