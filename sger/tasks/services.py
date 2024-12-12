from .models import Task

def create_task(description, start_date, end_date, status):
    task = Task(
        description=description,
        start_date=start_date,
        end_date=end_date,
        status=status,
    )
    task.save()
    return task

def get_task_by_description(partial_description):
    try:
        task = Task.objects.get(description__icontains=partial_description)
        return task
    except Task.MultipleObjectsReturned:
        return Task.objects.filter(description__icontains=partial_description)
    except Task.DoesNotExist:
        return None

def get_all_tasks():
    return Task.objects.all()
