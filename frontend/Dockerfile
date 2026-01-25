FROM nginx:alpine

# Frontend dosyalarını kopyala
COPY . /usr/share/nginx/html

# Nginx config
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
