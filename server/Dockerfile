# Base image
FROM python:3.12-slim

# Prevent Python from writing pyc files and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies (including PostgreSQL dev libraries and Graphviz)
RUN apt-get update && apt-get install -y \
    graphviz \
    gcc \
    libpq-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install gunicorn

# Copy project files
COPY . /app/

# Create directory for static files
RUN mkdir -p /app/staticfiles

# Environment variables for production (usually provided via docker-compose)
# ENV DEBUG=False

# Note: collectstatic is typically run during the build or at runtime
# RUN python manage.py collectstatic --noinput

# Expose the application port
EXPOSE 8000

# Use Gunicorn as the production WSGI server
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
