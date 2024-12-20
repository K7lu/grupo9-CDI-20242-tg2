
from django.urls import path
from . import views
from .views import login_view, register_view

urlpatterns = [
    path('', views.home_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('usuarios/', views.usuarios_view, name='usuarios'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),

    # Rotas de clientes
    path('clientes/', views.clients_list, name='clients_list'),
    path('clientes/editar/<int:client_id>/', views.edit_client_view, name='edit_client'),
    path('clientes/buscar/', views.clients_search_view, name='clients_search'),

    # Rotas de projetos
    path('projetos/', views.projetos_view, name='projetos'),
    path('projetos/editar/<int:project_id>/', views.edit_project_view, name='edit_project'),
    path('projetos/excluir/<int:project_id>/', views.delete_project_view, name='delete_project'),

    # Rotas de departamentos
    path('departamentos/register/', views.department_register_view, name='department_register'),
    path('departamentos/', views.department_list_view, name='departments_list'),
    path('departamentos/search/', views.departments_search_view, name='departments_search'),
    path('departamentos/edit/<int:id>/', views.edit_department_view, name='edit_department'),
    path('departamentos/delete/<int:id>/', views.delete_department_view, name='delete_department'),

    # Rotas de contatos
    path('contatos/', views.contacts_view, name='contatos'),

     #Rotas de Funcionários
    path('funcionarios/cadastrar/', views.cadastrar_funcionario_view, name='funcionarios'),
    path('funcionarios/excluir/<int:id>/', views.excluir_funcionario_view, name='excluir_funcionario'),
    path('funcionarios/edit<int:id>', views.editar_funcionario_view, name='editar_funcionario'),

    # Rotas de Tarefas
    path('tarefas/', views.tarefas_view, name='tarefas'),
    path('tarefas/editar/<int:id>/', views.edit_task_view, name='edit_tasks'),
    path('tarefas/excluir/<int:id>/', views.delete_task_view, name='delete_tasks'),

    path('recursos/', views.recursos_view, name='recursos'),
    path('alocacoes/', views.alocacoes_view, name='alocacoes'),
]
