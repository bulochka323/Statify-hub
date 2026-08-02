FROM python:3.13-slim

WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements from bot folder
COPY bot/requirements.txt ./requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

# Copy bot code INTO a subfolder (щоб не засмічувати корінь /app)
COPY bot/ ./bot/

# Switch working directory inside /app/bot
WORKDIR /app/bot

# Create logs directory
RUN mkdir -p logs

# Expose port for render.com
EXPOSE 10000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:10000/api/v1/health || exit 1

# Run bot + API server
CMD ["sh", "-c", "python main.py & uvicorn api.handlers:app --host 0.0.0.0 --port 10000"]