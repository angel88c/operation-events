# ============================================================================
# Streamlit Professional Template — Dockerfile
# ============================================================================
# Build:
#   docker build -t streamlit-app .
#
# Run:
#   docker run -p 8501:8501 --env-file .env streamlit-app
#
# Run on custom port:
#   docker run -p 3001:8501 --env-file .env streamlit-app
# ============================================================================

FROM python:3.11-slim

# Prevent Python from writing .pyc files and enable unbuffered output
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies required by some Python packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies first (layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# The .streamlit/config.toml is copied from the project (via COPY . .)
# It already includes server, theme, browser, and client settings.

# 1. Asegúrate de que el puerto coincida
EXPOSE 3001

# 2. Corregimos el HEALTHCHECK para que apunte al puerto correcto
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:3001/_stcore/health || exit 1

# 3. IMPORTANTE: Agregamos los flags necesarios para que Streamlit 
# acepte conexiones externas en el puerto 3001
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=3001", "--server.address=0.0.0.0"]
