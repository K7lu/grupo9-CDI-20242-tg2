from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_departments, name='department_list'),
    path('create/', views.create_department_view, name='create_department'),
]
