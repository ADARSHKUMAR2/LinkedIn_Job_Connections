# Use an official uv + Python 3.12 slim image from GitHub Container Registry
# This avoids Docker Hub authentication issues in CI/CD pipelines
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

# Set working directory
WORKDIR /app

# Copy dependency files first to leverage Docker caching layers
COPY pyproject.toml uv.lock ./

# Install dependencies strictly from the lockfile without installing the project package itself
RUN uv sync --frozen --no-install-project

# Copy the rest of the application code
COPY . .

# Expose the port FastAPI runs on
EXPOSE 8000

# Run the FastAPI server using uv to ensure it hits the correct virtual environment
CMD ["uv", "run", "fastapi", "run", "app/main.py", "--host", "0.0.0.0", "--port", "8000"]