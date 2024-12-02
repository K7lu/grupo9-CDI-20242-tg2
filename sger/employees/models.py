from django.db import models

class Funcionario(models.Model):
    Nome = models.CharField(max_length=100)
    CPF = models.CharField(max_length=11, unique=True)
    Data_Contratacao = models.DateField(null=True, blank=True)
    Telefone = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.Nome
