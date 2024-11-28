# clients/views.py
from django.shortcuts import render

def home(request):
    return render(request, 'clients/home.html')
