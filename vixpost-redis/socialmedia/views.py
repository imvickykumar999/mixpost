from django.http import JsonResponse
from .tasks import check_and_run_scheduled_tasks

def run_scheduled_tasks_view(request):
    check_and_run_scheduled_tasks.delay()
    return JsonResponse({"status": "Scheduled tasks triggered"})
