from .models import ScheduledTask
from django.utils.timezone import now
from celery import shared_task
from mastodon import Mastodon
import requests
import os

from dotenv import load_dotenv
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

MASTODON_ACCESS_TOKEN = os.getenv("MASTODON_ACCESS_TOKEN")
MASTODON_CLIENT_ID = os.getenv("MASTODON_CLIENT_ID")
MASTODON_CLIENT_SECRET = os.getenv("MASTODON_CLIENT_SECRET")

@shared_task
def my_custom_task(task_id):
    try:
        task = ScheduledTask.objects.get(id=task_id)
        task_name = task.name
        caption = task.caption or ""
        image_path = task.media.path  # Assumes ImageField
    except ScheduledTask.DoesNotExist:
        task_name = f"Unknown task (ID: {task_id})"
        caption = ""
        image_path = None

    # --- Send Telegram message ---
    telegram_text = f"Running scheduled task: {task_name}"
    print(telegram_text)

    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    telegram_payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": telegram_text
    }

    try:
        telegram_response = requests.post(telegram_url, data=telegram_payload)
        telegram_response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Failed to send Telegram message: {e}")

    # --- Mastodon Upload and Post ---
    try:
        mastodon = Mastodon(
            client_id=MASTODON_CLIENT_ID,
            client_secret=MASTODON_CLIENT_SECRET,
            access_token=MASTODON_ACCESS_TOKEN,
            api_base_url='https://mastodon.social'
        )

        if image_path and os.path.exists(image_path):
            media = mastodon.media_post(image_path, "image/png")
            media_id = media['id']

            post = mastodon.status_post(
                status=caption,
                media_ids=[media_id]
            )
            print(f"Mastodon post created: {post['url']}")
        else:
            print("No valid image found for Mastodon post.")

    except Exception as e:
        print(f"Failed to post on Mastodon: {e}")

@shared_task
def check_and_run_scheduled_tasks():
    tasks = ScheduledTask.objects.filter(executed=False, run_at__lte=now())
    for task in tasks:
        my_custom_task.delay(task.id)
        task.executed = True
        task.save()
