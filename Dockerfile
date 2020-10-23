FROM nginx:stable-alpine

RUN apk add --no-cache \
    bash \
    openssl \
    py3-pip \
    python3 \
    rsync

RUN mkdir -p /etc/nginx/conf.d
COPY app/nginx.conf /etc/nginx/nginx.conf

WORKDIR /app
COPY app /app
COPY html /app/html

RUN python3 -m pip install -r requirements.txt

ENTRYPOINT ["bash", "docker-entrypoint.sh"]
