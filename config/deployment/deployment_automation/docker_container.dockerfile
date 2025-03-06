# Use official Python image as base
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project to the container
COPY . .

# Expose API ports
EXPOSE 5000  # REST API
EXPOSE 50051 # gRPC API

# Command to run the application
CMD ["python", "interfaces_api/rest_api.py"]
