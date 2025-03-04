#!/bin/bash

echo "🚀 Setting up Φ(a)-Optimized AI Execution Engine..."
echo "-------------------------------------------"

# Detect OS
OS_TYPE=$(uname)
if [[ "$OS_TYPE" == "Linux" ]]; then
    echo "Detected Linux 🐧"
elif [[ "$OS_TYPE" == "Darwin" ]]; then
    echo "Detected macOS 🍏"
elif [[ "$OS_TYPE" =~ "MINGW" || "$OS_TYPE" =~ "CYGWIN" ]]; then
    echo "Detected Windows 🖥️ (Using WSL or Git Bash)"
else
    echo "Unsupported OS: $OS_TYPE"
    exit 1
fi

# Install dependencies
echo "🔧 Installing dependencies..."
python3 -m pip install --upgrade pip
pip3 install -r requirements.txt

# Verify installation
echo "✅ Installation complete! Running initial test..."
python3 -c "import torch; print('✔ PyTorch Installed:', torch.__version__)"

echo "-------------------------------------------"
echo "🚀 You can now run AI models with Φ(a)-Optimized execution!"
