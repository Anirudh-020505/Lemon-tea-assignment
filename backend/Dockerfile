FROM python:3.10-slim

# Install system dependencies required for PyMuPDF (fitz) and building python packages
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create cache directory for FlashRank to persist models
RUN mkdir -p /app/flashrank_cache

# Copy application source
COPY . .

# Expose port
EXPOSE 8000

# Start Uvicorn with dynamic port mapping
CMD sh -c "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"
