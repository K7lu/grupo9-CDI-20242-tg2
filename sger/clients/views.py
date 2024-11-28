from django.shortcuts import render
from .models import Client
from .services import create_client

def client_list(request):
    clients = Client.objects.all()
    return render(request, 'clients/client_list.html', {'clients': clients})

def create_client_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        cnpj = request.POST.get('cnpj')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        
        create_client(name, cnpj, address, phone)
        
        return redirect('clients:client_list')
    
    return render(request, 'clients/create_client.html')
