from .models import ScheduledTask
from datetime import datetime
from django.utils.timezone import now
from celery import shared_task
import requests

TELEGRAM_BOT_TOKEN = "6297291074:AAFqSTe03EPfLeKuyeN4Q3lzlYTY2xI2j48"
TELEGRAM_CHAT_ID = "5721393154"  # Replace with your actual chat ID

@shared_task
def my_custom_task(task_id):
    try:
        task = ScheduledTask.objects.get(id=task_id)
        task_name = task.name
    except ScheduledTask.DoesNotExist:
        task_name = f"Unknown task (ID: {task_id})"

    text = f"Running scheduled task: {task_name}"
    print(text)

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text
    }

    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Failed to send Telegram message: {e}")

@shared_task
def check_and_run_scheduled_tasks():
    tasks = ScheduledTask.objects.filter(executed=False, run_at__lte=now())
    for task in tasks:
        my_custom_task.delay(task.id)  # Call your real task
        task.executed = True
        task.save()
