# Stage 1: Build Frontend React App
FROM node:20-alpine AS frontend-builder
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

# Stage 2: Python Backend Runtime
FROM python:3.11-slim
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy backend requirements & install
COPY backend/requirements.txt ./backend/requirements.txt
RUN pip install --no-cache-dir -r backend/requirements.txt

# Copy backend code & pre-built frontend dist
COPY backend/ ./backend/
COPY --from=frontend-builder /app/frontend/dist ./frontend/dist

# Expose port
EXPOSE 8000

# Set working directory to backend & start server
WORKDIR /app/backend
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
