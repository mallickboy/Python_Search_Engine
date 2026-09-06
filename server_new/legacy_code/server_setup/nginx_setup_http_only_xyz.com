# sudo nano /etc/nginx/sites-available/pysearch.mallickboy.com 
server { # http only
    listen 80;
    server_name pysearch.mallickboy.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }
}