# ===========================
# 1) Base Image
# ===========================
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# ===========================
# 2) Install dependencies
# ===========================
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Install gunicorn (production WSGI server)
RUN pip install gunicorn

# ===========================
# 3) Copy application code
# ===========================
COPY . .

# ===========================
# 4) Expose Flask port
# ===========================
EXPOSE 5000

# ===========================
# 5) Healthcheck (professor requires it)
# ===========================
HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl --fail http://localhost:5000/health || exit 1

# ===========================
# 6) Start command (Gunicorn)
# ===========================
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:create_app()"]
