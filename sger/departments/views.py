from django.shortcuts import render, redirect
from .models import Department
from .forms import DepartmentForm

def list_departments(request):
    departments = Department.objects.all()
    return render(request, 'departments/department_list.html', {'departments': departments})

def create_department_view(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('department_list')
    else:
        form = DepartmentForm()
    return render(request, 'departments/department_form.html', {'form': form})
