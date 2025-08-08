from .models import ScheduledTask
from datetime import datetime
from django.utils.timezone import now
from celery import shared_task

@shared_task
def my_custom_task(task_id):
    print(f"Running task with ID {task_id}")

@shared_task
def check_and_run_scheduled_tasks():
    tasks = ScheduledTask.objects.filter(executed=False, run_at__lte=now())
    for task in tasks:
        my_custom_task.delay(task.id)  # Call your real task
        task.executed = True
        task.save()
