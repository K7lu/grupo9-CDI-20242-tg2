from django.urls import path
from . import views
from .views import login_view, register_view
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', views.home_view, name='home'),  
    path('login/', views.login_view, name='login'),
    path('usuarios/', views.usuarios_view, name='usuarios'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('clientes/', views.clientes_view, name='clientes'),
    path('projetos/', views.projetos_view, name='projetos'),
    path('contatos/', views.contatos_view, name='contatos'),
    path('tarefas/', views.tarefas_view, name='tarefas'),
    path('recursos/', views.recursos_view, name='recursos'),
    path('funcionarios/', views.funcionarios_view, name='funcionarios'),
    path('alocacoes/', views.alocacoes_view, name='alocacoes'),
    path('departamentos/', views.departamentos_view, name='departamentos'),

]
