FROM python:3.11-slim

# Install curl for healthcheck (optional but recommended)
RUN apt-get update && apt-get install -y curl

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

# Copy application code
COPY . .

# Azure expects port 8000
EXPOSE 8000

# Healthcheck using curl
HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl --fail http://localhost:8000/health || exit 1

# Start gunicorn on port 8000, using app.factory
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--factory", "app:create_app"]
