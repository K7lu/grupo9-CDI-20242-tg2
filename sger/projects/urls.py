from django.urls import path
from . import views

urlpatterns = [
    path('projects_manager/', views.projects_manager, name='projects_manager'),
    path('projects/', views.projects_list, name='projects_list'),
    path('projects_register/', views.projects_register, name='projects_register'),
    path('projects_list/', views.projects_list, name='projects_list'),
    path('projects/delete/<int:id>', views.delete_projects_view, name='delete_project'),
    path('projects/edit/<int:id>/', views.edit_project_view, name='edit_project'),
    path('projects/search/', views.projects_search_view, name='projects_search'),
]
