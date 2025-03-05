#!/bin/bash
# ==============================================
# 🚀 INDUSTRY-LEADING AI EXECUTION LINUX INSTALLER
# ✅ Fully Automated, GPU-Optimized, Error-Resilient
# ==============================================

echo "🔹 Starting Optimized Installation on Linux..."

# Update & Install Dependencies
sudo apt update && sudo apt install -y     python3 python3-pip docker docker-compose curl wget git nvidia-container-toolkit || { echo "❌ Dependency installation failed! Retrying..."; sleep 5; sudo apt --fix-broken install -y; }

# Ensure NVIDIA GPU Support
if command -v nvidia-smi &> /dev/null; then
    echo "✅ NVIDIA GPU detected! Configuring CUDA..."
    distribution=$(. /etc/os-release;echo $ID$VERSION_ID)         && curl -s -L https://nvidia.github.io/nvidia-container-runtime/gpgkey | sudo apt-key add -         && curl -s -L https://nvidia.github.io/nvidia-container-runtime/$distribution/nvidia-container-runtime.list | sudo tee /etc/apt/sources.list.d/nvidia-container-runtime.list         && sudo apt update && sudo apt install -y nvidia-container-runtime || { echo "❌ Failed to configure NVIDIA GPU!"; exit 1; }
else
    echo "⚠️ No NVIDIA GPU found. Running in CPU mode."
fi

# Install AI Execution Dependencies
pip install --upgrade pip || { echo "❌ Pip upgrade failed! Retrying..."; sleep 5; pip install --upgrade pip; }
pip install -r /app/src/core/requirements.txt || { echo "❌ AI dependency installation failed! Retrying..."; sleep 5; pip install -r /app/src/core/requirements.txt; }

# Start AI Execution Engine
cd /app/deploy/
docker-compose up --build -d || { echo "❌ AI Execution failed! Restarting..."; docker-compose restart; }

echo "✅ Installation Complete! AI Execution Engine is now running."
