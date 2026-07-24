FROM python:3.12-slim

# Prevent Python from writing .pyc files and enable unbuffered logging
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8080

WORKDIR /app

# Install system dependencies required for OpenCV
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1-mesa-glx \
    libglib2.0-0 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy locked dependencies and install
COPY requirements.lock.txt /app/
RUN pip install --no-cache-dir -r requirements.lock.txt

# Copy application source code
COPY . /app/

# Create non-root user and temporary directory
RUN useradd -m -u 1000 appuser && \
    mkdir -p /tmp/styleai && \
    chown -R appuser:appuser /app /tmp/styleai

USER appuser

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8080/healthz || exit 1

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "2", "--threads", "4", "--timeout", "90", "wsgi:application"]
