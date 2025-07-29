# Use a lightweight Python base image
FROM python:3.10-slim-bullseye

# Prevents interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Install required system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends --no-install-suggests \
    build-essential \
    ffmpeg \
    libsm6 \
    libxext6 \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Upgrade pip, setuptools, and wheel
RUN python3 -m pip install --upgrade pip setuptools wheel

# Copy dependency list first (for layer caching)
COPY ./requirements.txt /app

# Install Python dependencies
RUN pip install --no-cache-dir --requirement /app/requirements.txt

# Copy rest of the application code
COPY . /app

# Set default command
CMD ["python3", "consumer.py"]