FROM python:3.13-alpine AS build
WORKDIR /build
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN python scripts/build.py

FROM nginx:1.29-alpine
# Python API for the EU-miner agreement (listens on 127.0.0.1:8081 behind nginx).
RUN apk add --no-cache python3 py3-pip font-dejavu su-exec \
 && python3 -m venv /opt/venv \
 && addgroup -S api && adduser -S -H -D -G api -s /sbin/nologin api
COPY requirements-api.txt /tmp/requirements-api.txt
RUN /opt/venv/bin/pip install --no-cache-dir -r /tmp/requirements-api.txt && rm /tmp/requirements-api.txt
COPY api/mine_eu /app/api/mine_eu
COPY legal /app/legal
COPY docker/entrypoint.sh /entrypoint.sh
ENV PYTHONPATH=/app/api PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 LEGAL_DIR=/app/legal
COPY --from=build /build/dist/ /usr/share/nginx/html/
COPY --from=build /build/dist/nginx.conf /etc/nginx/nginx.conf
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=3s CMD wget -q -O /dev/null http://127.0.0.1:8080/healthz || exit 1
ENTRYPOINT ["/entrypoint.sh"]
