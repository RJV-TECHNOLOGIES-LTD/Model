# ==============================================
# 🚀 INDUSTRY-LEADING AI EXECUTION PACKAGE MANAGER
# ✅ Self-Healing, Automated, Platform-Independent
# ==============================================

import os
import subprocess

REQUIREMENTS_FILE = "/app/src/core/requirements.txt"

def install_packages():
    """ Install AI execution dependencies with auto-recovery """
    print("📦 Installing AI dependencies...")

    try:
        subprocess.run(["pip", "install", "--upgrade", "pip"], check=True)
        subprocess.run(["pip", "install", "-r", REQUIREMENTS_FILE], check=True)
        print("✅ AI dependencies installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Dependency installation failed! Retrying... {e}")
        subprocess.run(["pip", "install", "-r", REQUIREMENTS_FILE], check=True)

if __name__ == "__main__":
    install_packages()
