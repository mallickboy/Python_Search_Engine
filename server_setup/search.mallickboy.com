# sudo nano /etc/nginx/sites-available/search.mallickboy.com

server {                                        # Redirect HTTP traffic to HTTPS
    listen 80;
    server_name search.mallickboy.com;
    return 301 https://$host$request_uri;       # Redirect to HTTPS
}

server {                                        # HTTPS Configuration
    listen 443 ssl http2;
    server_name search.mallickboy.com;

    ssl_certificate /etc/letsencrypt/live/search.mallickboy.com/fullchain.pem;    # SSL certificate paths 
    ssl_certificate_key /etc/letsencrypt/live/search.mallickboy.com/privkey.pem;

    ssl_protocols TLSv1.2 TLSv1.3;              # SSL security settings
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    
    location / {                                # proxy requests to flask app
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }
}