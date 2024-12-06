from django.urls import path
from . import views

urlpatterns = [
    path('tasks_manager/', views.tasks_manager, name='tasks_manager'),
]
