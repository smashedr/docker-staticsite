FROM nginx:stable-alpine

RUN apk add --no-cache \
    bash \
    openssl \
    py3-pip \
    python3

WORKDIR /app

COPY app/requirements.txt .
RUN python3 -m pip install -r requirements.txt

COPY app /app
COPY html /app/html

ENTRYPOINT ["bash", "docker-entrypoint.sh"]
