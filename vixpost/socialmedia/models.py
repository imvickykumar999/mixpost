from django.db import models

class ScheduledTask(models.Model):
    name = models.CharField(max_length=100)
    run_at = models.DateTimeField()
    executed = models.BooleanField(default=False)
    
    # New fields
    caption = models.TextField(blank=True, null=True)
    media = models.FileField(
        upload_to='scheduled_media/', 
        blank=True, 
        null=True,
        help_text="Upload image/video/gif"
    )

    url_generated = models.URLField(
        blank=True,
        null=True,
        help_text="Mastodon URL after successful post"
    )

    def __str__(self):
        return self.name
