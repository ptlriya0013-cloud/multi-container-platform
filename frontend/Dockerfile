FROM nginx:1.27-alpine

COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY index.html /usr/share/nginx/html/index.html

EXPOSE 80

HEALTHCHECK --interval=5s --timeout=3s --retries=5 \
    CMD wget -qO- http://127.0.0.1/ > /dev/null || exit 1
