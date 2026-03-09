FROM python:3.14.3-alpine3.23

RUN apk upgrade --no-cache

WORKDIR /app

RUN addgroup -S appgroup && \
    adduser -S -G appgroup -h /app -s /sbin/nologin appuser

COPY --chown=appuser:appgroup requirements.txt .
RUN pip install --upgrade pip --no-cache-dir -r requirements.txt

COPY --chown=appuser:appgroup . .

USER appuser

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "3", "wsgi:app"]

