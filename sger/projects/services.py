from .models import Project

def create_client(name, description, start_date, end_date):
    project = Project(
        name=name,
        description=description,
        start_date=start_date,
        end_date=end_date
    )
    project.save()
    return project

def get_project_by_name(name):
    try:
        project = Project.objects.get(name=name)
        return project
    except Project.DoesNotExist:
        return None

def get_all_projects():
    return Project.objects.all()