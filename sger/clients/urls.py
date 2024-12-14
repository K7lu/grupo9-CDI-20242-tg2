from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Página inicial da app 'clients'
    path('clients_list/', views.clients_list, name='clients_list'),
    path('clients_register/', views.clients_register_view, name='clients_register'),
    path('delete/<int:id>', views.delete_clients_view, name='delete_client'),
    path('client/edit/<int:id>/', views.edit_client_view, name='edit_client'),
    path('client/search/', views.clients_search_view, name='clients_search'),

    # Rotas de autenticação
    path('login/', views.login_view, name='login'),        # Página de login
    path('register/', views.register_view, name='register'),  # Página de registro
    path('logout/', views.logout_view, name='logout'),     # Logout
]
