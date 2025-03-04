#!/bin/bash
set -e

echo "Updating system packages..."
sudo apt update && sudo apt upgrade -y

echo "Installing Python dependencies..."
pip install -r requirements.txt

if ! command -v docker &> /dev/null; then
    echo "Installing Docker..."
    sudo apt install docker.io -y
fi

echo "Setting up virtual environment..."
python -m venv env
source env/bin/activate

echo "Running setup script..."
python setup.py install

echo "Installation completed successfully!"
