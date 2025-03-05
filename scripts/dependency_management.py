# ==============================================
# 🚀 INDUSTRY-LEADING DEPENDENCY MANAGEMENT FOR AI EXECUTION
# ✅ Automatic Installation, Error Recovery, and Multi-Platform Support
# ==============================================

import os
import subprocess
import sys
import logging
import json
import time
import pip
from typing import List

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

# Define dependencies and requirements
REQUIREMENTS_FILE = "/app/requirements.txt"
LOG_FILE = "/var/log/dependency_management.log"
ERROR_LOG_FILE = "/var/log/dependency_management_error.log"

# Max retry attempts for dependency installation
MAX_RETRY_ATTEMPTS = 3
RETRY_DELAY = 5  # seconds

# ---------------------------------------------------------------
# Function to check for existing dependencies
# ---------------------------------------------------------------
def check_existing_dependencies():
    """Check installed dependencies to avoid redundant installations."""
    installed = {pkg.key for pkg in pip.get_installed_distributions()}
    logging.info("🔹 Checking existing dependencies...")

    with open(REQUIREMENTS_FILE, "r") as f:
        required_packages = [line.strip() for line in f.readlines() if line.strip() and not line.startswith("#")]

    missing_packages = [pkg for pkg in required_packages if pkg not in installed]
    if missing_packages:
        logging.info(f"⚠️ Missing packages: {missing_packages}")
    else:
        logging.info("✅ All required dependencies are already installed.")
    
    return missing_packages

# ---------------------------------------------------------------
# Function to install missing dependencies
# ---------------------------------------------------------------
def install_dependencies(missing_packages: List[str]):
    """Install missing dependencies from the requirements.txt file."""
    logging.info("🔹 Installing missing dependencies...")

    for pkg in missing_packages:
        attempts = 0
        while attempts < MAX_RETRY_ATTEMPTS:
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])
                logging.info(f"✅ Successfully installed {pkg}")
                break
            except subprocess.CalledProcessError as e:
                logging.error(f"❌ Installation failed for {pkg}: {e}")
                attempts += 1
                if attempts >= MAX_RETRY_ATTEMPTS:
                    logging.error(f"❌ Failed to install {pkg} after {MAX_RETRY_ATTEMPTS} attempts.")
                else:
                    logging.info(f"🔄 Retrying installation of {pkg} (Attempt {attempts + 1}/{MAX_RETRY_ATTEMPTS})")
                    time.sleep(RETRY_DELAY)

# ---------------------------------------------------------------
# Function to update existing dependencies
# ---------------------------------------------------------------
def update_dependencies():
    """Update existing dependencies to the latest versions."""
    logging.info("🔹 Updating existing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "-r", REQUIREMENTS_FILE])
        logging.info("✅ All dependencies updated successfully.")
    except subprocess.CalledProcessError as e:
        logging.error(f"❌ Error while updating dependencies: {e}")

# ---------------------------------------------------------------
# Function to track the installation of dependencies
# ---------------------------------------------------------------
def track_dependency_installation():
    """Track the installation of dependencies and log errors."""
    with open(LOG_FILE, "a") as log, open(ERROR_LOG_FILE, "a") as error_log:
        log.write(f"Dependency installation started at {time.strftime('%Y-%m-%d %H:%M:%S')}\n")

    try:
        missing_packages = check_existing_dependencies()
        if missing_packages:
            install_dependencies(missing_packages)
        else:
            update_dependencies()

    except Exception as e:
        logging.error(f"❌ Error during dependency installation: {e}")
        with open(ERROR_LOG_FILE, "a") as error_log:
            error_log.write(f"Error during installation: {str(e)}\n")

    with open(LOG_FILE, "a") as log:
        log.write(f"Dependency installation completed at {time.strftime('%Y-%m-%d %H:%M:%S')}\n")

# ---------------------------------------------------------------
# Function to check if all dependencies were installed successfully
# ---------------------------------------------------------------
def verify_dependencies():
    """Verify that all dependencies were installed successfully."""
    logging.info("🔹 Verifying installed dependencies...")

    with open(REQUIREMENTS_FILE, "r") as f:
        required_packages = [line.strip() for line in f.readlines() if line.strip() and not line.startswith("#")]

    installed = {pkg.key for pkg in pip.get_installed_distributions()}
    missing_packages = [pkg for pkg in required_packages if pkg not in installed]
    
    if missing_packages:
        logging.error(f"❌ Missing dependencies: {missing_packages}")
        return False
    else:
        logging.info("✅ All dependencies installed successfully.")
        return True

# ---------------------------------------------------------------
# Function to handle custom error logging for failed dependency installs
# ---------------------------------------------------------------
def log_failed_dependencies(failed_packages: List[str]):
    """Log the details of failed dependency installations."""
    if failed_packages:
        logging.error(f"❌ Failed to install the following dependencies: {failed_packages}")
        with open(ERROR_LOG_FILE, "a") as error_log:
            error_log.write(f"Failed to install dependencies: {failed_packages}\n")
    else:
        logging.info("✅ All dependencies installed without errors.")

# ---------------------------------------------------------------
# Main function to run the dependency management process
# ---------------------------------------------------------------
def main():
    """Main function to manage the installation, verification, and logging of dependencies."""
    logging.info("🚀 Starting Dependency Management for AI Execution...")

    track_dependency_installation()

    # Verify if all dependencies are installed correctly
    if verify_dependencies():
        logging.info("✅ All dependencies are installed and verified.")
    else:
        logging.error("❌ There were issues with installing dependencies. Check the error logs for more details.")

if __name__ == "__main__":
    main()
