# Dockerfile for User Management Plugin
# Single-responsibility: Run user_management plugin only
# Includes all required dependencies for this specific plugin

FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

# Install system dependencies for this plugin
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy plugin requirements
COPY requirements.txt .

# Install plugin dependencies
RUN pip install --upgrade pip setuptools wheel && \
    pip install -r requirements.txt

# Copy plugin code
COPY user_management/ ./user_management/
COPY setup.py .
COPY README.md .
COPY LICENSE .

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "from user_management.models import User; print('OK')" || exit 1

# Default command
CMD ["python", "-m", "user_management"]
