server {
    listen 80;
    server_name 115.159.86.190; # 这是HOST机器的外部域名，用地址也行

    location / {
        proxy_pass http://127.0.0.1:8080; # 这里是指向 gunicorn host 的服务地址
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

  }