FROM nginx:stable-alpine
ENV TZ=America/Los_Angeles

RUN apk add --no-cache \
    bash \
    py3-pip \
    python3 \
    rsync

RUN mkdir -p /etc/nginx/conf.d
COPY docker/nginx.conf /etc/nginx/nginx.conf

WORKDIR /docker
COPY docker /docker
COPY html /docker/html

RUN python3 -m pip install -r requirements.txt

ENTRYPOINT ["sh", "docker-entrypoint.sh"]
