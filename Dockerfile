# Multi-stage Dockerfile for Full-Stack AI Apps

# Python backend stage
FROM python:3.9-slim as python-backend

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy Python requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy Python source code
COPY src/ ./src/
COPY aws/ ./aws/
COPY gcp/ ./gcp/
COPY azure/ ./azure/
COPY examples/ ./examples/

# Node.js frontend stage
FROM node:18-alpine as node-frontend

WORKDIR /app

# Copy package files
COPY package.json package-lock.json ./

# Install Node.js dependencies
RUN npm ci --only=production

# Copy Node.js source code
COPY src/ ./src/

# Production stage
FROM python:3.9-slim as production

WORKDIR /app

# Install system dependencies for production
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Copy installed Python packages from python-backend stage
COPY --from=python-backend /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=python-backend /usr/local/bin /usr/local/bin

# Copy Node.js modules from node-frontend stage
COPY --from=node-frontend /app/node_modules ./node_modules

# Copy application code
COPY --chown=appuser:appuser src/ ./src/
COPY --chown=appuser:appuser aws/ ./aws/
COPY --chown=appuser:appuser gcp/ ./gcp/
COPY --chown=appuser:appuser azure/ ./azure/
COPY --chown=appuser:appuser examples/ ./examples/
COPY --chown=appuser:appuser package.json ./

# Create logs directory
RUN mkdir -p logs

# Expose ports
EXPOSE 8000 3000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Default command (can be overridden)
CMD ["python", "src/main.py"]

# Development stage
FROM production as development

USER root

# Install development dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Install development tools
RUN apt-get update && apt-get install -y \
    vim \
    htop \
    && rm -rf /var/lib/apt/lists/*

USER appuser

# Enable hot reloading for development
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]