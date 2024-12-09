# sger/urls.py
from django.contrib import admin
from django.urls import path, include
from clients import views as client_views

urlpatterns = [
    path('admin/', admin.site.urls),                     # Admin
    path('', client_views.home, name='home'),            # Página inicial
    path('clients/', include('clients.urls')),           # URLs de clients
    path('employees/', include('employees.urls')),       # URLs de employees
    path('departments/', include('departments.urls')),   # URLs de departments
    path('projects/', include('projects.urls')),         # URLs de projects
    path('tasks/', include('tasks.urls')),               # URLs de tasks

]
