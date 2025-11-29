FROM python:3.11-slim

# Install curl (needed for healthcheck)
RUN apt-get update && apt-get install -y curl

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

COPY . .

# Azure listens on port 8000
EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl --fail http://localhost:8000/health || exit 1

# Correct Gunicorn factory syntax (NO --factory)
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:create_app()"]
