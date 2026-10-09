FROM python:3.13-alpine AS build
WORKDIR /build
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN python scripts/build.py

FROM nginx:1.29-alpine
COPY --from=build /build/dist/ /usr/share/nginx/html/
COPY --from=build /build/dist/nginx.conf /etc/nginx/nginx.conf
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=3s CMD wget -q -O /dev/null http://127.0.0.1:8080/healthz || exit 1
