from django.shortcuts import render, redirect
from .forms import ProjectForm
from .services import create_project, list_projects

def project_registration(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            create_project(form.cleaned_data)
            return redirect('project_list')
    else:
        form = ProjectForm()
    return render(request, 'projects/register.html', {'form': form})

def project_list(request):
    projects = list_projects()
    return render(request, 'projects/list.html', {'projects': projects})