from django.urls import path
from . import views

urlpatterns = [
    path('projects_manager/', views.projects_manager, name='projects_manager'),
]
