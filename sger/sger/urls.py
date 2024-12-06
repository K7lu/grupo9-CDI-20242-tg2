# sger/urls.py
from django.contrib import admin
from django.urls import path, include
from clients import views 
from employees import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'), 
    path('clients/', include('clients.urls')),
    path('employee_registration/', views.employee_registration, name='employee_registration'),
    path('projects/', include('projects.urls')),
]
