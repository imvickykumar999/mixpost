# [`VixPost`](https://vixpost.imvickykumar999.online/admin/)`/admin`

<img width="1535" height="888" alt="image" src="https://github.com/user-attachments/assets/28ec5fe0-98ba-4073-9c8a-d071d00295d2" />

---

- `sudo nano /etc/nginx/sites-available/vixpost`

```
server {
    listen 80;
    server_name vixpost.imvickykumar999.online;

    # Redirect all HTTP requests to HTTPS
    location / {
        return 301 https://$host$request_uri;
    }
}

server {
    listen 443 ssl;
    server_name vixpost.imvickykumar999.online;

    ssl_certificate /etc/letsencrypt/live/vixpost.imvickykumar999.online/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/vixpost.imvickykumar999.online/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

    # Serve static files
    location /static/ {
        alias /root/projects/vixpost/staticfiles/;
        expires max;
        access_log off;
    }

    # Serve media files
    location /media/ {
        alias /root/projects/vixpost/media/;
        expires max;
        access_log off;
    }

    # Proxy pass to Gunicorn/Django app
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }
}
```

- `sudo nano /etc/systemd/system/celery.service`

```
[Unit]
Description=Celery Worker Service
After=network.target

[Service]
User=root
Group=root
WorkingDirectory=/root/projects/vixpost
Environment="PATH=/root/projects/vixpost/.venv/bin"
ExecStart=/root/projects/vixpost/.venv/bin/celery -A vixpost worker --loglevel=info --pool=solo

Restart=always

[Install]
WantedBy=multi-user.target
```

- `sudo nano /etc/systemd/system/celerybeat.service`

```
[Unit]
Description=Celery Beat Service
After=network.target

[Service]
User=root
Group=root
WorkingDirectory=/root/projects/vixpost
Environment="PATH=/root/projects/vixpost/.venv/bin"
ExecStart=/root/projects/vixpost/.venv/bin/celery -A vixpost beat --loglevel=info

Restart=always

[Install]
WantedBy=multi-user.target
```

- `sudo nano /etc/systemd/system/gunicorn.service`

```
[Unit]
Description=gunicorn daemon for vixpost
After=network.target

[Service]
User=root
Group=www-data
WorkingDirectory=/root/projects/vixpost
ExecStart=/root/projects/vixpost/.venv/bin/gunicorn --workers 3 --bind 127.0.0.1:8000 vixpost.wsgi:application

[Install]
WantedBy=multi-user.target
```
