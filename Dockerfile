# Use official Python slim image
FROM python:3.11-slim

# Set environment variables to ensure Python outputs are sent straight to terminal (no buffering)
ENV PYTHONUNBUFFERED=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR='/var/cache/pypoetry'

# Set working directory
WORKDIR /app

# Install system dependencies for poetry and building packages
RUN apt-get update && apt-get install -y curl build-essential

# Install Poetry (latest stable)
RUN curl -sSL https://install.python-poetry.org | python3 -

# Add Poetry to PATH
ENV PATH="/root/.local/bin:$PATH"

# Copy only poetry files to leverage Docker cache
COPY poetry.lock pyproject.toml /app/

# Install dependencies via Poetry (no virtualenvs)
RUN poetry install --no-interaction --no-ansi --no-root

# Copy the rest of the application code
COPY . /app

# Expose port 8000 for FastAPI
EXPOSE 1234

# Run the app with uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "1234"]
