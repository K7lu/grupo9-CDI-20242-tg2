from django.urls import path
from . import views

urlpatterns = [
    path('tasks_manager/', views.tasks_manager, name='tasks_manager'),
    path('tasks_register/', views.tasks_register, name='tasks_register'),
    path('tasks_list/', views.tasks_list, name='tasks_list'),
    path('tasks/delete/<int:id>', views.delete_tasks_view, name='delete_task'),
    path('tasks/edit/<int:id>/', views.edit_task_view, name='edit_task'),
    path('tasks/search/', views.tasks_search_view, name='tasks_search'),
]
