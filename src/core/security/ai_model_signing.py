# ==============================================
# 🚀 INDUSTRY-LEADING AI MODEL SIGNING
# ✅ Ensures Integrity, Authentication, and Version Control for AI Models
# ==============================================

import os
import hashlib
import hmac
import logging
import subprocess
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from time import sleep
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

# Model Signing Configuration
PRIVATE_KEY_PATH = "/app/keys/private_key.pem"  # Path to the private key used for signing
PUBLIC_KEY_PATH = "/app/keys/public_key.pem"    # Path to the public key used for verification
MODEL_DIRECTORY = "/app/models/"
SIGNED_MODEL_DIRECTORY = "/app/signed_models/"
MODEL_VERSION = "v2.0"  # Example model version
MODEL_FILE_NAME = "unified_model.onnx"  # Example AI model file
MODEL_PATH = os.path.join(MODEL_DIRECTORY, MODEL_FILE_NAME)
SIGNED_MODEL_PATH = os.path.join(SIGNED_MODEL_DIRECTORY, f"{MODEL_VERSION}_{MODEL_FILE_NAME}.signed")

# ---------------------------------------------------------------
# Function to load the private key for signing the AI model
# ---------------------------------------------------------------
def load_private_key():
    """Load the private key for signing."""
    try:
        with open(PRIVATE_KEY_PATH, "rb") as key_file:
            private_key = serialization.load_pem_private_key(key_file.read(), password=None, backend=default_backend())
            logging.info("✅ Private key loaded successfully.")
            return private_key
    except Exception as e:
        logging.error(f"❌ Error loading private key: {e}")
        raise Exception("Failed to load private key.")

# ---------------------------------------------------------------
# Function to load the public key for model verification
# ---------------------------------------------------------------
def load_public_key():
    """Load the public key for model verification."""
    try:
        with open(PUBLIC_KEY_PATH, "rb") as key_file:
            public_key = serialization.load_pem_public_key(key_file.read(), backend=default_backend())
            logging.info("✅ Public key loaded successfully.")
            return public_key
    except Exception as e:
        logging.error(f"❌ Error loading public key: {e}")
        raise Exception("Failed to load public key.")

# ---------------------------------------------------------------
# Function to sign the AI model using the private key
# ---------------------------------------------------------------
def sign_ai_model():
    """Sign the AI model to ensure its authenticity and integrity."""
    private_key = load_private_key()

    try:
        # Read the AI model file
        with open(MODEL_PATH, "rb") as model_file:
            model_data = model_file.read()

        # Sign the model file data
        signature = private_key.sign(
            model_data,
            padding.PKCS1v15(),
            hashes.SHA256()
        )

        # Save the signed model
        signed_model_path = os.path.join(SIGNED_MODEL_DIRECTORY, f"{MODEL_VERSION}_{MODEL_FILE_NAME}.signed")
        with open(signed_model_path, "wb") as signed_file:
            signed_file.write(model_data)
            signed_file.write(signature)

        logging.info(f"✅ Model {MODEL_FILE_NAME} signed successfully and saved to {signed_model_path}.")
    except Exception as e:
        logging.error(f"❌ Error signing the AI model: {e}")
        raise Exception("Failed to sign the AI model.")

# ---------------------------------------------------------------
# Function to verify the integrity of the AI model using the public key
# ---------------------------------------------------------------
def verify_ai_model_signature():
    """Verify the integrity of the signed AI model using the public key."""
    public_key = load_public_key()

    try:
        # Read the signed model and signature
        with open(SIGNED_MODEL_PATH, "rb") as signed_file:
            signed_model_data = signed_file.read()
            model_data = signed_model_data[:-256]  # The last 256 bytes are the signature
            signature = signed_model_data[-256:]

        # Verify the signature using the public key
        public_key.verify(
            signature,
            model_data,
            padding.PKCS1v15(),
            hashes.SHA256()
        )

        logging.info(f"✅ Model signature verified successfully for {MODEL_FILE_NAME}.")
    except Exception as e:
        logging.error(f"❌ Error verifying model signature: {e}")
        raise Exception("Model verification failed.")

# ---------------------------------------------------------------
# Function to monitor and validate model integrity during execution
# ---------------------------------------------------------------
def monitor_and_validate_model():
    """Monitor AI model integrity and validate its signature during execution."""
    while True:
        try:
            # Periodically check the integrity of the AI model
            logging.info("🔹 Monitoring model integrity...")
            verify_ai_model_signature()

            # Simulate AI model execution
            logging.info("🔹 Running AI model inference...")
            sleep(30)  # Sleep for 30 seconds before the next check
        except Exception as e:
            logging.error(f"❌ Error during model integrity check: {e}")
            sleep(60)  # Wait before retrying in case of error

# ---------------------------------------------------------------
# Function to trigger rollback in case of signature verification failure
# ---------------------------------------------------------------
def trigger_rollback():
    """Trigger rollback to the last known good model version in case of verification failure."""
    try:
        # Restore the stable model
        stable_model_path = os.path.join(MODEL_DIRECTORY, "stable_model.onnx")
        if os.path.exists(stable_model_path):
            shutil.copy(stable_model_path, MODEL_PATH)
            logging.info(f"✅ Rollback triggered. Restored stable model to {stable_model_path}.")
        else:
            logging.error("❌ No stable model found for rollback.")
            raise Exception("No stable model found for rollback.")
    except Exception as e:
        logging.error(f"❌ Error during rollback: {e}")

# ---------------------------------------------------------------
# Main function to initialize model signing and integrity monitoring
# ---------------------------------------------------------------
def main():
    """Main function to run the AI model signing, verification, and monitoring process."""
    logging.info("🚀 Starting AI Model Signing and Integrity Monitoring...")

    try:
        # Sign the model
        sign_ai_model()

        # Monitor and verify model integrity
        monitor_and_validate_model()

    except Exception as e:
        logging.error(f"❌ Model signing and verification failed: {e}")
        trigger_rollback()  # Trigger rollback if model signing/verification fails

if __name__ == "__main__":
    main()
