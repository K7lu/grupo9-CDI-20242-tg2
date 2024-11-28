# sger/urls.py
from django.contrib import admin
from django.urls import path, include
from clients import views 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'), 
    path('clients/', include('clients.urls')),
]
