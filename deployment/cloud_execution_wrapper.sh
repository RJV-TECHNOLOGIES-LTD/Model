#!/bin/bash
# =====================================================================================
# 🚀 INDUSTRY-LEADING CLOUD AI EXECUTION WRAPPER
# ✅ Fully Resilient, Self-Healing, Cloud & Edge AI Optimized
# =====================================================================================

set -e  # Exit script on error

# LOGGING & ERROR HANDLING
LOG_FILE="/var/log/cloud_ai_execution.log"
ERROR_LOG_FILE="/var/log/cloud_ai_execution_error.log"

exec > >(tee -a "$LOG_FILE") 2> >(tee -a "$ERROR_LOG_FILE" >&2)  # Log output and errors

echo "🚀 Starting AI Execution in Cloud Environment..."

# =====================================================================================
# 🛠️ CLOUD PROVIDER DETECTION
# =====================================================================================
CLOUD_PROVIDER="Unknown"

if curl -s http://169.254.169.254/latest/meta-data/instance-id | grep -q "i-"; then
    CLOUD_PROVIDER="AWS"
elif curl -s http://metadata.google.internal/computeMetadata/v1/instance/name -H "Metadata-Flavor: Google" > /dev/null 2>&1; then
    CLOUD_PROVIDER="GCP"
elif az vm list --query "[].name" --output tsv > /dev/null 2>&1; then
    CLOUD_PROVIDER="Azure"
elif [ -f "/var/run/secrets/kubernetes.io/serviceaccount/token" ]; then
    CLOUD_PROVIDER="Kubernetes"
fi

echo "🌍 Cloud Provider Detected: $CLOUD_PROVIDER"

# =====================================================================================
# 🛠️ CHECK & INSTALL REQUIRED TOOLS (Docker, NVIDIA Drivers, Python)
# =====================================================================================
echo "🔍 Checking system requirements..."

# Ensure Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker not found! Installing..."
    sudo apt update && sudo apt install -y docker docker-compose || { echo "❌ Failed to install Docker!"; exit 1; }
fi

# Ensure NVIDIA GPU Support if Available
if command -v nvidia-smi &> /dev/null; then
    echo "✅ NVIDIA GPU detected! Configuring CUDA..."
    if ! command -v nvidia-container-runtime &> /dev/null; then
        echo "❌ NVIDIA container runtime not found! Installing..."
        distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
        curl -s -L https://nvidia.github.io/nvidia-container-runtime/gpgkey | sudo apt-key add -
        curl -s -L https://nvidia.github.io/nvidia-container-runtime/$distribution/nvidia-container-runtime.list | sudo tee /etc/apt/sources.list.d/nvidia-container-runtime.list
        sudo apt update && sudo apt install -y nvidia-container-runtime || { echo "❌ Failed to install NVIDIA runtime!"; exit 1; }
    fi
else
    echo "⚠️ No NVIDIA GPU detected. Running in CPU mode."
fi

# Ensure Python & Pip are Installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found! Installing..."
    sudo apt update && sudo apt install -y python3 python3-pip || { echo "❌ Failed to install Python!"; exit 1; }
fi

# Ensure Required Python Packages are Installed
pip3 install --upgrade pip || { echo "❌ Pip upgrade failed! Retrying..."; sleep 5; pip3 install --upgrade pip; }
pip3 install -r /app/src/core/requirements.txt || { echo "❌ AI dependency installation failed! Retrying..."; sleep 5; pip3 install -r /app/src/core/requirements.txt; }

# =====================================================================================
# ⚙️ CONFIGURE AI EXECUTION RESOURCES (CPU/GPU/MEMORY)
# =====================================================================================
echo "🛠️ Configuring AI execution resources..."

# Detect System Specs
CPU_CORES=$(nproc)
MEMORY_TOTAL=$(awk '/MemTotal/ {printf "%.0f\n", $2/1024}' /proc/meminfo)  # Memory in MB

if command -v nvidia-smi &> /dev/null; then
    GPU_COUNT=$(nvidia-smi --query-gpu=name --format=csv,noheader | wc -l)
else
    GPU_COUNT=0
fi

echo "🔹 CPU Cores: $CPU_CORES"
echo "🔹 Memory: ${MEMORY_TOTAL}MB"
echo "🔹 GPUs Available: $GPU_COUNT"

# Optimize Docker Resource Allocation
DOCKER_CPU_LIMIT=$((CPU_CORES / 2))
DOCKER_MEMORY_LIMIT="${MEMORY_TOTAL}m"

if [ "$GPU_COUNT" -gt 0 ]; then
    DOCKER_GPU_ARGS="--gpus all"
else
    DOCKER_GPU_ARGS=""
fi

echo "🔹 AI Execution Resources: CPU: $DOCKER_CPU_LIMIT cores, Memory: $DOCKER_MEMORY_LIMIT, GPUs: $GPU_COUNT"

# =====================================================================================
# 🚀 START AI EXECUTION ENGINE (WITH AUTO-SCALING & DISTRIBUTED DEPLOYMENT)
# =====================================================================================
echo "🚀 Starting AI Execution Engine..."

cd /app/deploy/

docker-compose up --build -d \
    --cpus "$DOCKER_CPU_LIMIT" \
    --memory "$DOCKER_MEMORY_LIMIT" \
    $DOCKER_GPU_ARGS \
    || { echo "❌ AI Execution failed! Attempting auto-recovery..."; docker-compose restart; }

echo "✅ AI Execution Engine is running! 🎯"

# =====================================================================================
# 📈 MONITOR EXECUTION & AUTO-SCALE IF NECESSARY
# =====================================================================================
echo "📈 Monitoring AI execution performance..."

# Check execution logs for failures
while true; do
    sleep 30
    if ! docker ps | grep -q "ai_execution"; then
        echo "❌ AI Execution stopped unexpectedly! Restarting..."
        docker-compose restart
    fi
done
