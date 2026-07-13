from django.urls import path
from . import views
from .views import TaskCreateView, TaskUpdateView, TaskDetailView,CommentCreateView, TaskDeleteView

urlpatterns = [
    path('create/', TaskCreateView.as_view(), name='task-create'),
    path('<int:task_pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('<int:task_pk>/update', TaskUpdateView.as_view(), name='task-update'),
    path('<int:task_pk>/delete', TaskDeleteView.as_view(), name='task-delete'),
    path('<int:task_pk>/assign_task', views.assign_task_page, name='task-assign'),
    path('<int:task_pk>/assign_task/assigned', views.assign_task, name='task-assign-confirmed'),
    path('<int:task_pk>/comment/create', CommentCreateView.as_view(), name='comment-create'),
]