from django.urls import path

from .views import ProjectCreateView,ProjectUpdateView,ProjectDetailView,ProjectDeleteView



urlpatterns = [
    # path('team/<int:pk>/project/', team_detail_project, name='team-detail-project'),
    path('create/', ProjectCreateView.as_view(), name='project-create'),
    path('<int:project_pk>/update/', ProjectUpdateView.as_view(), name='project-update'),
    path('<int:project_pk>/delete/', ProjectDeleteView.as_view(), name='project-delete'),
    path('<int:project_pk>/', ProjectDetailView.as_view(), name='project-detail'),
]