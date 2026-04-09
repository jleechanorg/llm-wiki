FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY mvp_site/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# fastembed 0.7.4 defaults to /tmp/fastembed_cache which Cloud Run clears on every cold start.
# Force a persistent location inside the image so the pre-downloaded model survives.
# FASTEMBED_CACHE_PATH must be set BEFORE the download RUN steps so preflight scripts
# materialize model artifacts in the runtime cache directory.
ENV FASTEMBED_CACHE_PATH=/opt/fastembed_cache

# Provision the fastembed model cache during build (prefer GCS archive, fallback to HF).
# GCS vars are ARG-only (inline in RUN) to avoid persisting into the runtime image.
COPY scripts/preflight_model_docker.py /app/scripts/preflight_model_docker.py
ARG FASTEMBED_GCS_ARCHIVE_URI=""
ARG FASTEMBED_GCS_REQUIRED="false"
RUN FASTEMBED_GCS_ARCHIVE_URI=${FASTEMBED_GCS_ARCHIVE_URI} \
    FASTEMBED_GCS_REQUIRED=${FASTEMBED_GCS_REQUIRED} \
    python3 /app/scripts/preflight_model_docker.py

# Copy the infrastructure package (required by gunicorn.conf.py)
COPY infrastructure/ /app/infrastructure/

# Copy the application into a package directory so absolute imports like
# `from mvp_site import ...` continue to work in production images.
COPY mvp_site/ /app/mvp_site/

# Copy cache-busting script for build-time asset processing
COPY scripts/cache_busting.py /app/scripts/cache_busting.py
# Copy classifier preflight check (shared with run_local_server.sh)
COPY scripts/preflight_model.py /app/scripts/preflight_model.py

# Ensure Python can resolve both `mvp_site` and `infrastructure` packages
# CRITICAL: Must be set BEFORE cache_busting.py RUN (it imports from mvp_site)
ENV PYTHONPATH=/app

# Pre-download the fastembed model during build to avoid runtime downloads
# This uses the same shared preflight script as local startup.
RUN python3 /app/scripts/preflight_model.py

# Runtime guardrail: never perform HuggingFace network calls at startup.
# Model artifacts must come from pre-baked image cache.
ENV HF_HUB_OFFLINE=1

# Apply cache-busting during image build to ensure hashed assets are included
# This runs INSIDE the Docker build, guaranteeing hashed files are in the final image
# (prevents .gitignore exclusion issues with gcloud builds submit)
RUN python3 /app/scripts/cache_busting.py /app/mvp_site/frontend_v1 || exit 1

WORKDIR /app/mvp_site

# Production-optimized Gunicorn configuration with gthread workers
# Configuration file provides: workers, threads, timeout, logging, and lifecycle management
# Performance: 12+ concurrent requests vs 1 request with default sync worker
# Requires infrastructure package for worker configuration helpers
CMD ["gunicorn", "-c", "gunicorn.conf.py", "main:create_app()"]
