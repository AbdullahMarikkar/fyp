# 🛠 Stage 1: Build the dependencies in a separate image
FROM python:3.12.7-slim AS base

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0

# Create a virtual environment to store dependencies
WORKDIR /venv
RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"

# Copy only the requirements file to cache the dependencies
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# -------------------------------------------------------------------------

# 🎯 Stage 2: Build the final application
FROM python:3.12.7-slim

# Set working directory
WORKDIR /app

# Install system dependencies again (small size, cached from first stage)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy virtual environment from the previous stage
COPY --from=base /venv /venv
ENV PATH="/venv/bin:$PATH"

# Copy only the application code (not reinstalling dependencies)
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Run FastAPI with Uvicorn
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
