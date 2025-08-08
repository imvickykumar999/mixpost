# from .models import ScheduledTask
# from django.utils.timezone import now
# from celery import shared_task
# from mastodon import Mastodon
# import requests, os, time

# from dotenv import load_dotenv
# load_dotenv()

# TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
# TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# MASTODON_ACCESS_TOKEN = os.getenv("MASTODON_ACCESS_TOKEN")
# MASTODON_CLIENT_ID = os.getenv("MASTODON_CLIENT_ID")
# MASTODON_CLIENT_SECRET = os.getenv("MASTODON_CLIENT_SECRET")


# def upload_and_post(task_name, caption, media_path):
#     # --- Telegram message ---
#     telegram_text = f"Running scheduled task: {task_name}"
#     print(f"Sending to Telegram: {telegram_text}")

#     telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
#     telegram_payload = {
#         "chat_id": TELEGRAM_CHAT_ID,
#         "text": telegram_text
#     }

#     try:
#         telegram_response = requests.post(telegram_url, data=telegram_payload)
#         telegram_response.raise_for_status()
#         print("Telegram message sent successfully.")
#     except requests.exceptions.RequestException as e:
#         print(f"Failed to send Telegram message: {e}")

#     # --- Mastodon upload and post ---
#     try:
#         mastodon = Mastodon(
#             client_id=MASTODON_CLIENT_ID,
#             client_secret=MASTODON_CLIENT_SECRET,
#             access_token=MASTODON_ACCESS_TOKEN,
#             api_base_url='https://mastodon.social'
#         )

#         if media_path and os.path.exists(media_path):
#             print("Uploading media to Mastodon...")
#             media = mastodon.media_post(media_path)

#             # Wait for media processing to complete
#             media_id = media['id']
#             for _ in range(10):  # up to ~5 seconds
#                 media_status = mastodon.media(media_id)
#                 if media_status.get('url'):
#                     break
#                 time.sleep(0.5)

#             post = mastodon.status_post(
#                 status=caption,
#                 media_ids=[media_id]
#             )
#             print(f"Mastodon post created with media: {post['url']}")
#         else:
#             # No media, just post caption text
#             post = mastodon.status_post(status=caption)
#             print(f"Mastodon post created without media: {post['url']}")

#         return post  # ✅ Return the post object

#     except Exception as e:
#         print(f"Failed to post on Mastodon: {e}")
#         return None  # In case of failure


# @shared_task
# def my_custom_task(task_id):
#     try:
#         task = ScheduledTask.objects.get(id=task_id)
#         task_name = task.name
#         caption = task.caption or ""
#         media_path = task.media.path if task.media else None
#     except ScheduledTask.DoesNotExist:
#         print(f"Task with ID {task_id} not found.")
#         return

#     post = upload_and_post(task_name, caption, media_path)

#     if post and 'url' in post:
#         task.url_generated = post['url']  # ✅ Save the URL to the model
#         task.executed = True
#         task.save()
#         print(f"Saved Mastodon URL to task: {post['url']}")
#     else:
#         print("Post failed or no URL returned.")


# @shared_task
# def check_and_run_scheduled_tasks():
#     tasks = ScheduledTask.objects.filter(executed=False, run_at__lte=now())
#     for task in tasks:
#         my_custom_task.delay(task.id)
