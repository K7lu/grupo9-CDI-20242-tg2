from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db import IntegrityError
from .models import Funcionario 

def employee_registration(request):
    if request.method == "POST":
        nome = request.POST.get('nome')
        cpf = request.POST.get('cpf')
        data_contratacao = request.POST.get('data_contratacao')
        telefone = request.POST.get('telefone')

        try:
            Funcionario.objects.create(
                Nome=nome,
                CPF=cpf,
                Data_Contratacao=data_contratacao or None,  
                Telefone=telefone
            )
            return redirect('success_page') 
        except IntegrityError:
            return render(request, 'employee_registration.html', {
                'error_message': 'Erro: CPF já está registrado!'
            })

    return render(request, 'employee_registration.html')
