import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vixpost.settings')

app = Celery('vixpost')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'run-task-every-minute': {
        'task': 'socialmedia.tasks.check_and_run_scheduled_tasks',
        'schedule': crontab(minute='*/1'),
    },
}

app.conf.timezone = 'Asia/Kolkata'  # or UTC or your timezone

app.autodiscover_tasks()
