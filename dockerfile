FROM python:3.12.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN groupadd -r appgroup && \
    useradd -r -g appgroup -d /app -s /bin/false appuser

COPY --chown=appuser:appgroup . .

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "3", "wsgi:app"]

