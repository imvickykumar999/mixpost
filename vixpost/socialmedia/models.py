# models.py
from django.db import models

class ScheduledTask(models.Model):
    name = models.CharField(max_length=100)
    run_at = models.DateTimeField()
    executed = models.BooleanField(default=False)

    def __str__(self):
        return self.name
