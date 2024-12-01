from django.shortcuts import render

def projects_manager(request):
    # Lógica para exibir o formulário de cadastro de funcionários
    return render(request, 'projects_manager.html')
def home(request):
    return render(request, 'clients/home.html')
