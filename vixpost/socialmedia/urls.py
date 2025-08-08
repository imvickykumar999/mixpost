from django.urls import path
from .views import run_scheduled_tasks_view

urlpatterns = [
    path('', run_scheduled_tasks_view, name='run_scheduled_tasks'),
]
