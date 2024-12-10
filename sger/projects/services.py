from .models import Project
from django.db.models import Q

def create_project(name, description, start_date, end_date):
    project = Project(
        name=name,
        description=description,
        start_date=start_date,
        end_date=end_date
    )
    project.save()
    return project

def get_project_by_name(partial_name):
    try:
        project = Project.objects.get(name__icontains=partial_name)
        return project
    except Project.MultipleObjectsReturned:
        return Project.objects.filter(name__icontains=partial_name)
    except Project.DoesNotExist:
        return None

def get_all_projects():
    return Porject.objects.all()
