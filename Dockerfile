# 🐳 Sacred Geometry AAR Processor Container

FROM python:3.11-alpine

LABEL maintainer="Core-Framework Team"
LABEL version="1.0.0"
LABEL description="Sacred Geometry AAR Processor with real-time monitoring integration"

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV AAR_ENVIRONMENT=production
ENV SACRED_GEOMETRY_MODE=enabled

# Create app directory
WORKDIR /app

# Install system dependencies
RUN apk add --no-cache \
    gcc \
    musl-dev \
    postgresql-dev \
    libffi-dev \
    openssl-dev \
    curl \
    && rm -rf /var/cache/apk/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Create necessary directories
RUN mkdir -p /app/src \
             /app/templates \
             /app/config \
             /app/data \
             /app/logs \
             /app/sacred-geometry

# Copy application code
COPY src/ ./src/

# Copy entrypoint script
COPY entrypoint.sh /app/
RUN chmod +x /app/entrypoint.sh

# Create non-root user for security
RUN addgroup -g 1001 aar && \
    adduser -D -s /bin/sh -u 1001 -G aar aar && \
    chown -R aar:aar /app

# Switch to non-root user
USER aar

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Expose port
EXPOSE 8000

# Set entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]

# Default command
CMD ["python", "src/aar_processor.py"]
