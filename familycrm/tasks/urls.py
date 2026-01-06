from django.urls import path
from tasks import views

app_name = 'tasks'

urlpatterns = [
    path('', views.TaskListView.as_view(), name='index'),
    path('status/<slug:status>', views.TaskListViewByStatus.as_view(), name='status'),
    path('add_task/', views.AddTaskView.as_view(), name='add_task'),
    path('task/<int:pk>/', views.TaskDetailView.as_view(), name='task_detail'),
    path('task/make_task_in_progress/<int:pk>', views.MakeTaskInProgressView.as_view(), name='make_task_in_progress'),
    path('task/make_task_completed/<int:pk>', views.MakeTaskCompletedView.as_view(), name='make_task_completed'),
    path('task/edit/<int:pk>', views.EditTaskView.as_view(), name='edit_task'),
    path('task/delete/<int:pk>', views.DeleteTaskView.as_view(), name='delete_task'),
]
