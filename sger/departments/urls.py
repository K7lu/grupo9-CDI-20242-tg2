from django.urls import path
from . import views

urlpatterns = [
    path('department_register/', views.department_register_view, name='department_register'),
    path('department_list/', views.department_list_view, name='department_list'),
    path('departments/', views.departments_search_view, name='departments_search'),  # Lista e pesquisa
    path('departments/delete/<int:id>/', views.delete_department_view, name='delete_department'),  # Exclusão
    path('departments/edit/<int:id>/', views.edit_department_view, name='edit_department'),  # Edição
]
