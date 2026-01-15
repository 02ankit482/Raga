# -----------------------------
# Base image
# -----------------------------
FROM python:3.10-slim

# -----------------------------
# System dependencies
# -----------------------------
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    curl \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# -----------------------------
# Set working directory
# -----------------------------
WORKDIR /app

# -----------------------------
# Copy requirements first (better caching)
# -----------------------------
COPY requirements.txt .

# -----------------------------
# Install Python dependencies
# -----------------------------
RUN pip install --no-cache-dir -r requirements.txt

# -----------------------------
# Copy application code
# -----------------------------
COPY . .

# -----------------------------
# Expose port
# -----------------------------
EXPOSE 5000

# -----------------------------
# Run the app
# -----------------------------
CMD ["python", "run.py"]
