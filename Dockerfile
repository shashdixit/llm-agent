# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install prettier globally
RUN npm install -g prettier@3.4.2

# Copy the rest of the application
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Set environment variable for AI Proxy Token (to be passed at runtime)
ENV AIPROXY_TOKEN=""
ENV USER_EMAIL=""

# Command to run the application
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]