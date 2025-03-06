# Base image with CUDA support for GPU acceleration
FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu20.04

# Set working directory
WORKDIR /app

# Install Python dependencies
RUN apt-get update && apt-get install -y python3 python3-pip && \
    pip3 install --no-cache-dir \
        torch torchvision torchaudio \
        flask grpcio grpcio-tools protobuf \
        numpy pandas websocket-client \
        onnxruntime tensorflow tensorflow-lite

# Copy source files
COPY . .

# Expose API ports
EXPOSE 5000  # REST API
EXPOSE 50051 # gRPC API

# Set entrypoint
CMD ["python3", "interfaces_api/rest_api.py"]
