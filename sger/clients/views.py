# clients/views.py
from django.shortcuts import render

def home(request):
    return render(request, 'clients/home.html')

def clients_list(request):
    return render(request, 'clients/clients_list.html', {'clients': clients})