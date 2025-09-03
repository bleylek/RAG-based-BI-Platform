FROM python:3.10-slim AS builder

WORKDIR /app

# Install system dependencies required for building Python packages
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    libpq-dev \
    cmake \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create and activate virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Update pip and install build tools
RUN pip install --no-cache-dir --upgrade pip wheel setuptools

# Split requirements installation to leverage Docker caching
COPY requirements.txt .

# Install base packages
RUN pip install --no-cache-dir numpy scipy scikit-learn

# Install FAISS separately (large dependency)
RUN pip install --no-cache-dir faiss-cpu

# Install core Flask/web dependencies first
RUN pip install --no-cache-dir Flask Werkzeug Jinja2 itsdangerous click blinker gunicorn

# Install remaining requirements with more relaxed version constraints
RUN pip install --no-cache-dir -r requirements.txt

# Second stage - lightweight runtime image
FROM python:3.10-slim

WORKDIR /app

# Install only runtime dependencies and curl for healthcheck
RUN apt-get update && apt-get install -y \
    libpq-dev \
    poppler-utils \
    libmagic1 \
    libgl1 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create instance directory with proper permissions
RUN mkdir -p /app/instance && chmod 777 /app/instance

# Copy virtual environment from builder stage
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy application code with proper ordering for caching
COPY run.py .
COPY app ./app/
COPY rag_store ./rag_store/
COPY .env* ./

# Create necessary directories
RUN mkdir -p rag_store/uploads

# Create a non-root user
RUN groupadd -g 1000 appgroup && \
    useradd -u 1000 -g appgroup -m -s /bin/bash appuser
    
# Give proper permissions to instance directory and rag_store
RUN chown -R appuser:appgroup /app
RUN chmod -R 777 /app/instance
RUN chmod -R 755 /app/rag_store

# Switch to non-root user
USER appuser

# Application port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=10s --retries=3 \
  CMD curl -f http://localhost:5000/ || exit 1

# Environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Runtime command
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--threads", "4", "--timeout", "120", "run:app"]
