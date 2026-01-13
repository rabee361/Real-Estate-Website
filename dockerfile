# Use a slim Python image
FROM python:3.12-slim-bookworm

# Install system dependencies for PostGIS and building packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    binutils \
    libproj-dev \
    gdal-bin \
    libgdal-dev \
    python3-gdal \
    libpq-dev \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set working directory
WORKDIR /app

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies using uv
# --frozen ensures we use the exact versions from uv.lock
RUN uv sync --frozen --no-install-project

# Copy the rest of the application
COPY . .

# Finalize the project installation (installing the project itself in the venv)
RUN uv sync --frozen

# Expose the Django port
EXPOSE 8000

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/app/.venv/bin:$PATH"

# Default command
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
