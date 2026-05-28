# Production-ready Docker containerization for Recruitment Intelligence Platform
FROM python:3.12-slim

# Set system environments
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=5000

# Set workspace directory
WORKDIR /app

# Install system dependencies (including standard build tools)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements list
COPY requirements.txt /app/

# Install python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy source codes
COPY . /app/

# Expose port
EXPOSE 5000

# Run uvicorn/gunicorn server on startup
CMD ["python", "app.py"]
