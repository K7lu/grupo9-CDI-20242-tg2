from django.shortcuts import render

def tasks_manager(request):
    # Lógica para exibir o formulário de cadastro de funcionários
    return render(request, 'tasks_manager.html')
def home(request):
    return render(request, 'clients/home.html')
