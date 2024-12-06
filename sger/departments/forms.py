from django import forms
from .models import Department  # Certifique-se de que o modelo Department existe

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'description']  # Substitua pelos campos do modelo
