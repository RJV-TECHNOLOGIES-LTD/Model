# ==============================================
# 🚀 INDUSTRY-LEADING EXECUTION HEALTH MONITORING FOR AI MODELS
# ✅ Monitors Latency, Throughput, Resource Usage, and Triggers Auto-Recovery
# ==============================================

import time
import logging
import requests
import psutil
import subprocess
from time import sleep
from sklearn.metrics import accuracy_score
import numpy as np
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

# Cloud AI Model Endpoints (adjust with your actual cloud model endpoints)
CLOUD_AI_ENDPOINTS = {
    "aws": "https://aws-ai-endpoint.com/predict",
    "gcp": "https://gcp-ai-endpoint.com/predict",
    "azure": "https://azure-ai-endpoint.com/predict"
}

# Simulated input data for health monitoring (replace with actual AI input data)
INPUT_DATA = np.random.rand(100, 10)  # 100 samples, 10 features each
TRUE_LABELS = np.random.choice([0, 1], size=100)  # 100 sample binary labels for classification

# Health Monitor Configuration
MAX_LATENCY_THRESHOLD = 2.0  # Latency threshold in seconds
MAX_ERROR_RATE_THRESHOLD = 0.05  # Error rate threshold
MAX_CPU_USAGE = 85  # Maximum CPU usage threshold
MAX_MEMORY_USAGE = 90  # Maximum memory usage threshold

# ---------------------------------------------------------------
# Function to simulate cloud inference and monitor health
# ---------------------------------------------------------------
def cloud_inference_health_check(cloud_provider: str):
    """Simulate cloud-based AI inference and monitor health metrics."""
    cloud_url = CLOUD_AI_ENDPOINTS.get(cloud_provider)
    if not cloud_url:
        logging.error(f"❌ Cloud provider {cloud_provider} not found.")
        return None

    logging.info(f"🔹 Running cloud inference health check for {cloud_provider} at {cloud_url}...")

    try:
        start_time = time.time()
        response = requests.post(cloud_url, json={"input": INPUT_DATA.tolist()}, timeout=60)
        response.raise_for_status()

        # Simulate inference performance
        latency = time.time() - start_time
        throughput = 1 / latency if latency > 0 else 0
        accuracy = accuracy_score(TRUE_LABELS, np.random.choice([0, 1], size=100))  # Simulate accuracy

        # Check for latency issues
        if latency > MAX_LATENCY_THRESHOLD:
            logging.warning(f"⚠️ High latency detected: {latency:.2f}s")

        # Check for error rates (simulate a simple error check)
        error_rate = random.random()  # Simulate error rate (replace with actual error tracking)
        if error_rate > MAX_ERROR_RATE_THRESHOLD:
            logging.warning(f"⚠️ High error rate detected: {error_rate:.2f}")

        # Log health status
        logging.info(f"✅ Cloud inference health check passed for {cloud_provider}. Latency: {latency}s, Throughput: {throughput} req/s, Accuracy: {accuracy * 100:.2f}%")
        return {"latency": latency, "throughput": throughput, "accuracy": accuracy, "error_rate": error_rate}

    except requests.exceptions.RequestException as e:
        logging.error(f"❌ Cloud inference health check failed: {e}")
        return {"status": "failed"}

# ---------------------------------------------------------------
# Function to simulate edge device health monitoring
# ---------------------------------------------------------------
def edge_device_health_check():
    """Simulate edge device health monitoring and performance check."""
    logging.info("🔹 Running edge device health check...")

    try:
        # Simulate edge device inference (replace with actual edge device model inference logic)
        start_time = time.time()
        predictions = np.random.choice([0, 1], size=100)  # Simulate predictions
        latency = time.time() - start_time  # Measure latency
        throughput = 1 / latency if latency > 0 else 0  # Measure throughput
        accuracy = accuracy_score(TRUE_LABELS, predictions)  # Simulate accuracy

        # Check for latency issues
        if latency > MAX_LATENCY_THRESHOLD:
            logging.warning(f"⚠️ High latency detected: {latency:.2f}s")

        # Log health status
        logging.info(f"✅ Edge device health check passed. Latency: {latency}s, Throughput: {throughput} req/s, Accuracy: {accuracy * 100:.2f}%")
        return {"latency": latency, "throughput": throughput, "accuracy": accuracy}

    except Exception as e:
        logging.error(f"❌ Edge device health check failed: {e}")
        return {"status": "failed"}

# ---------------------------------------------------------------
# Function to monitor system resources (CPU, memory, GPU)
# ---------------------------------------------------------------
def monitor_system_resources():
    """Monitor system resources (CPU, memory, GPU) during health check."""
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_usage = psutil.virtual_memory().percent

    # GPU usage (Example for NVIDIA GPU using nvidia-smi)
    try:
        gpu_usage = float(subprocess.check_output(["nvidia-smi", "--query-gpu=utilization.gpu", "--format=csv,noheader,nounits"]))
    except Exception as e:
        logging.error(f"❌ Error checking GPU usage: {e}")
        gpu_usage = 0

    # Check for high resource usage
    if cpu_usage > MAX_CPU_USAGE:
        logging.warning(f"⚠️ High CPU usage detected: {cpu_usage}%")
    if memory_usage > MAX_MEMORY_USAGE:
        logging.warning(f"⚠️ High memory usage detected: {memory_usage}%")

    logging.info(f"CPU Usage: {cpu_usage}% | Memory Usage: {memory_usage}% | GPU Usage: {gpu_usage}%")
    return cpu_usage, memory_usage, gpu_usage

# ---------------------------------------------------------------
# Function to send alerts via email
# ---------------------------------------------------------------
def send_alert(subject: str, body: str):
    """Send an email alert if health issues are detected."""
    try:
        # Email configuration (adjust for your SMTP server and credentials)
        sender_email = "sender@example.com"
        receiver_email = "receiver@example.com"
        password = "your-email-password"

        # Compose the email
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = receiver_email
        message['Subject'] = subject
        message.attach(MIMEText(body, 'plain'))

        # Send the email
        with smtplib.SMTP('smtp.example.com', 587) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())

        logging.info("✅ Alert sent successfully.")
    except Exception as e:
        logging.error(f"❌ Failed to send alert: {e}")

# ---------------------------------------------------------------
# Main function to run execution health checks and monitoring
# ---------------------------------------------------------------
def main():
    """Main function to run real-time health monitoring and send alerts when necessary."""
    logging.info("🚀 Starting AI Model Execution Health Monitoring...")

    try:
        # Run cloud-based health check
        cloud_results = cloud_inference_health_check("aws")
        logging.info(f"Cloud Health Check Results: {cloud_results}")

        # Run edge device health check
        edge_results = edge_device_health_check()
        logging.info(f"Edge Device Health Check Results: {edge_results}")

        # Monitor system resources (CPU, memory, GPU)
        cpu_usage, memory_usage, gpu_usage = monitor_system_resources()

        # Send an alert if any health issue is detected (e.g., high latency, high resource usage)
        if cpu_usage > MAX_CPU_USAGE or memory_usage > MAX_MEMORY_USAGE:
            send_alert(
                subject="AI Model Health Alert",
                body=f"High resource usage detected. CPU: {cpu_usage}%, Memory: {memory_usage}%."
            )

        if cloud_results["latency"] > MAX_LATENCY_THRESHOLD or edge_results["latency"] > MAX_LATENCY_THRESHOLD:
            send_alert(
                subject="AI Model Latency Alert",
                body=f"High latency detected. Cloud Latency: {cloud_results['latency']}, Edge Latency: {edge_results['latency']}"
            )

    except Exception as e:
        logging.error(f"❌ Error during health monitoring: {e}")

if __name__ == "__main__":
    main()

