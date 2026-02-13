# TrueFace - Deepfake Detection
# Docker Image for Production Deployment

FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV TF_CPP_MIN_LOG_LEVEL=2

# Set working directory
WORKDIR /app

# Install minimal system dependencies for opencv-python-headless
RUN apt-get update && apt-get install -y --no-install-recommends \
    libglib2.0-0 \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create uploads directory
RUN mkdir -p uploads

# Expose port
EXPOSE 5000

# Health check (using wget which is available in slim image, or python)
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/')" || exit 1

# Run with gunicorn
CMD ["gunicorn", "--chdir", "backend", "app:app", "--bind", "0.0.0.0:5000", "--timeout", "120", "--workers", "1"]
