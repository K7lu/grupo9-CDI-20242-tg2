from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from clients import views as client_views

urlpatterns = [
    path('register/', client_views.register_view, name='register'),  # Rota para registro
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', auth_views.LoginView.as_view(template_name='login.html'), name='home'),
    path('clients/', include('clients.urls')),
    path('employees/', include('employees.urls')),
    path('departments/', include('departments.urls')),
    path('projects/', include('projects.urls')),
    path('tasks/', include('tasks.urls')),
]
