from django.shortcuts import render

def employee_registration(request):
    # Lógica para exibir o formulário de cadastro de funcionários
    return render(request, 'employee_registration.html')
def home(request):
    return render(request, 'clients/home.html')
