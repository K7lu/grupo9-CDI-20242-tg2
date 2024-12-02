from django.urls import path
from . import views

urlpatterns = [
    path('project_registration/', views.project_registration, name='project_registration'),
]
