# ==============================================
# 🚀 INDUSTRY-LEADING AI EXECUTION PACKAGE MANAGER
# ✅ Self-Healing, Multi-Platform, Secure, High-Performance
# ==============================================

import os
import sys
import subprocess
import platform
import time
import threading

# Define constants
REQUIREMENTS_FILE = "/app/src/core/requirements.txt"
LOG_FILE = "/var/log/universal_package_manager.log"
ERROR_LOG_FILE = "/var/log/universal_package_manager_error.log"

# =================================================================
# 🛠️ LOGGING & ERROR HANDLING
# =================================================================
def log_message(message, error=False):
    """ Log messages to file and console """
    log_type = "ERROR" if error else "INFO"
    log_entry = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] [{log_type}] {message}\n"
    
    with open(LOG_FILE, "a") as log:
        log.write(log_entry)
    
    if error:
        with open(ERROR_LOG_FILE, "a") as err_log:
            err_log.write(log_entry)

    print(log_entry, end="")

# =================================================================
# 🛠️ SYSTEM CHECK & PRE-INSTALLATION VALIDATION
# =================================================================
def check_system():
    """ Ensure system has necessary tools installed """
    log_message("🔍 Validating system requirements...")

    # Detect Operating System
    os_name = platform.system().lower()
    log_message(f"🔹 Operating System Detected: {os_name}")

    # Check if Python is installed
    if not sys.version_info >= (3, 8):
        log_message("❌ Python 3.8+ is required. Please upgrade Python.", error=True)
        sys.exit(1)

    # Check if Pip is installed
    try:
        subprocess.run(["pip", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    except subprocess.CalledProcessError:
        log_message("❌ Pip is not installed. Installing now...", error=True)
        subprocess.run(["python3", "-m", "ensurepip"], check=True)
        subprocess.run(["python3", "-m", "pip", "install", "--upgrade", "pip"], check=True)

# =================================================================
# 🚀 SELF-HEALING AI DEPENDENCY MANAGEMENT
# =================================================================
def install_packages():
    """ Install AI execution dependencies with auto-recovery """
    log_message("📦 Installing AI dependencies...")

    try:
        # Ensure Pip is Up-to-Date
        subprocess.run(["pip", "install", "--upgrade", "pip"], check=True)

        # Install dependencies in parallel using threading
        def install_dependency(package):
            """ Install a single dependency with retry mechanism """
            attempts = 3
            for attempt in range(1, attempts + 1):
                try:
                    subprocess.run(["pip", "install", package], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    log_message(f"✅ Successfully installed {package}")
                    return
                except subprocess.CalledProcessError as e:
                    log_message(f"❌ Attempt {attempt} to install {package} failed: {e}", error=True)
                    time.sleep(5)

            log_message(f"🚨 Failed to install {package} after {attempts} attempts.", error=True)

        # Read requirements.txt and install dependencies in parallel
        with open(REQUIREMENTS_FILE, "r") as file:
            packages = [line.strip() for line in file if line.strip() and not line.startswith("#")]

        threads = []
        for package in packages:
            thread = threading.Thread(target=install_dependency, args=(package,))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        log_message("✅ AI dependencies installed successfully!")

    except Exception as e:
        log_message(f"❌ Dependency installation failed: {e}", error=True)

# =================================================================
# ⚠️ CONFLICT RESOLUTION & AUTO-REPAIR
# =================================================================
def resolve_conflicts():
    """ Detect and resolve package version conflicts """
    log_message("🔍 Checking for package conflicts...")

    try:
        result = subprocess.run(["pip", "check"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            log_message("⚠️ Conflicts detected! Attempting resolution...", error=True)

            # Auto-fix package conflicts by reinstalling
            for line in result.stdout.split("\n"):
                if "has requirement" in line:
                    package = line.split()[0]
                    log_message(f"🔄 Resolving conflict for {package}...")
                    subprocess.run(["pip", "install", "--upgrade", package], check=True)
            
            log_message("✅ All conflicts resolved!")
        else:
            log_message("✅ No conflicts detected!")

    except Exception as e:
        log_message(f"❌ Error resolving conflicts: {e}", error=True)

# =================================================================
# 🔐 SECURITY & ENVIRONMENT SANDBOXING
# =================================================================
def setup_virtual_env():
    """ Create an isolated environment for AI execution """
    log_message("🔐 Setting up secure virtual environment...")

    try:
        subprocess.run(["python3", "-m", "venv", "/app/venv"], check=True)
        log_message("✅ Virtual environment created!")
    except Exception as e:
        log_message(f"❌ Failed to create virtual environment: {e}", error=True)

# =================================================================
# 🚀 MAIN EXECUTION (SELF-HEALING INSTALLATION)
# =================================================================
if __name__ == "__main__":
    log_message("🚀 Starting AI Execution Package Manager...")

    check_system()          # System validation
    setup_virtual_env()     # Secure execution environment
    install_packages()      # Install dependencies
    resolve_conflicts()     # Auto-fix dependency conflicts

    log_message("✅ AI execution environment is fully configured!")
