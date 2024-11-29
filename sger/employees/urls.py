from django.urls import path
from . import views

urlpatterns = [
    path('employee_registration/', views.employee_registration, name='employee_registration'),
]
