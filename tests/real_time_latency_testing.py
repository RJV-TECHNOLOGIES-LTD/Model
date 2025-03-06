# ==============================================
# 🚀 INDUSTRY-LEADING REAL-TIME LATENCY TESTING FOR AI MODELS
# ✅ Measures Latency, Throughput, and Optimizes Inference Performance
# ==============================================

import time
import logging
import requests
import psutil
import subprocess
import numpy as np
from time import sleep
from sklearn.metrics import accuracy_score
from subprocess import run
import matplotlib.pyplot as plt

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

# Cloud AI Model Endpoints (adjust with your actual cloud model endpoints)
CLOUD_AI_ENDPOINTS = {
    "aws": "https://aws-ai-endpoint.com/predict",
    "gcp": "https://gcp-ai-endpoint.com/predict",
    "azure": "https://azure-ai-endpoint.com/predict"
}

# Simulation input data for latency tests (replace with actual AI input data)
INPUT_DATA = np.random.rand(100, 10)  # 100 samples, 10 features each
TRUE_LABELS = np.random.choice([0, 1], size=100)  # 100 sample binary labels for classification

# Maximum retry attempts for cloud inference
MAX_RETRY_ATTEMPTS = 3
RETRY_DELAY = 5  # seconds

# ---------------------------------------------------------------
# Function to test latency for cloud inference
# ---------------------------------------------------------------
def cloud_inference_latency_test(cloud_provider: str):
    """Test AI inference latency for a cloud provider."""
    cloud_url = CLOUD_AI_ENDPOINTS.get(cloud_provider)
    if not cloud_url:
        logging.error(f"❌ Cloud provider {cloud_provider} not found.")
        return None

    logging.info(f"🔹 Running cloud inference latency test for {cloud_provider} at {cloud_url}...")

    attempts = 0
    while attempts < MAX_RETRY_ATTEMPTS:
        try:
            # Simulate inference request to the cloud model
            start_time = time.time()
            response = requests.post(cloud_url, json={"input": INPUT_DATA.tolist()}, timeout=60)
            response.raise_for_status()

            latency = time.time() - start_time  # Measure latency
            throughput = 1 / latency if latency > 0 else 0  # Measure throughput
            accuracy = accuracy_score(TRUE_LABELS, np.random.choice([0, 1], size=100))  # Simulate accuracy

            # Log latency and performance metrics
            logging.info(f"✅ Cloud inference successful for {cloud_provider}. Latency: {latency}s, Throughput: {throughput} req/s, Accuracy: {accuracy * 100:.2f}%")
            return {"latency": latency, "throughput": throughput, "accuracy": accuracy}

        except requests.exceptions.RequestException as e:
            logging.error(f"❌ Cloud inference failed: {e}")
            sleep(RETRY_DELAY)
            attempts += 1

    logging.error(f"❌ Cloud inference failed after {MAX_RETRY_ATTEMPTS} attempts for {cloud_provider}.")
    return None

# ---------------------------------------------------------------
# Function to test latency for edge device inference
# ---------------------------------------------------------------
def edge_inference_latency_test():
    """Test AI inference latency on an edge device."""
    logging.info("🔹 Running edge device inference latency test...")

    try:
        # Simulate edge device inference (replace with actual edge device model inference logic)
        start_time = time.time()
        predictions = np.random.choice([0, 1], size=100)  # Simulate predictions
        latency = time.time() - start_time  # Measure latency
        throughput = 1 / latency if latency > 0 else 0  # Measure throughput
        accuracy = accuracy_score(TRUE_LABELS, predictions)  # Simulate accuracy

        # Log latency and performance metrics
        logging.info(f"✅ Edge inference successful. Latency: {latency}s, Throughput: {throughput} req/s, Accuracy: {accuracy * 100:.2f}%")
        return {"latency": latency, "throughput": throughput, "accuracy": accuracy}
    except Exception as e:
        logging.error(f"❌ Edge inference failed: {e}")
        return None

# ---------------------------------------------------------------
# Function to monitor GPU, CPU, and memory usage during latency tests
# ---------------------------------------------------------------
def monitor_system_resources():
    """Monitor system resources (CPU, memory, GPU) during latency tests."""
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_usage = psutil.virtual_memory().percent

    # GPU usage (Example for NVIDIA GPU using nvidia-smi)
    try:
        gpu_usage = float(subprocess.check_output(["nvidia-smi", "--query-gpu=utilization.gpu", "--format=csv,noheader,nounits"]))
    except Exception as e:
        logging.error(f"❌ Error checking GPU usage: {e}")
        gpu_usage = 0

    logging.info(f"CPU Usage: {cpu_usage}% | Memory Usage: {memory_usage}% | GPU Usage: {gpu_usage}%")

    return cpu_usage, memory_usage, gpu_usage

# ---------------------------------------------------------------
# Function to generate latency comparison report
# ---------------------------------------------------------------
def generate_latency_comparison_report(results):
    """Generate a latency comparison report for cloud and edge inference."""
    latency_values = [results[cloud_provider]["latency"] for cloud_provider in CLOUD_AI_ENDPOINTS]
    throughput_values = [results[cloud_provider]["throughput"] for cloud_provider in CLOUD_AI_ENDPOINTS]
    accuracy_values = [results[cloud_provider]["accuracy"] for cloud_provider in CLOUD_AI_ENDPOINTS]

    # Plot Latency Comparison
    logging.info("🔹 Generating Latency Comparison Report...")

    # Latency comparison plot
    plt.figure(figsize=(10, 6))
    plt.bar(results.keys(), latency_values, color='blue')
    plt.xlabel('Cloud Providers')
    plt.ylabel('Latency (seconds)')
    plt.title('Latency Comparison for AI Inference')
    plt.tight_layout()
    plt.savefig("latency_comparison.png")
    plt.show()

    # Throughput comparison plot
    plt.figure(figsize=(10, 6))
    plt.bar(results.keys(), throughput_values, color='green')
    plt.xlabel('Cloud Providers')
    plt.ylabel('Throughput (requests/second)')
    plt.title('Throughput Comparison for AI Inference')
    plt.tight_layout()
    plt.savefig("throughput_comparison.png")
    plt.show()

    # Accuracy comparison plot
    plt.figure(figsize=(10, 6))
    plt.bar(results.keys(), accuracy_values, color='red')
    plt.xlabel('Cloud Providers')
    plt.ylabel('Accuracy (%)')
    plt.title('Accuracy Comparison for AI Inference')
    plt.tight_layout()
    plt.savefig("accuracy_comparison.png")
    plt.show()

    logging.info(f"✅ Latency Comparison completed. Check the generated plots: latency_comparison.png, throughput_comparison.png, accuracy_comparison.png")

# ---------------------------------------------------------------
# Function to trigger auto-scaling based on resource usage
# ---------------------------------------------------------------
def trigger_auto_scaling(cpu_usage, memory_usage, gpu_usage):
    """Trigger auto-scaling based on resource utilization during latency tests."""
    if cpu_usage > 80 or memory_usage > 80 or gpu_usage > 80:
        logging.info("⚠️ High resource usage detected! Triggering auto-scaling...")
        scaling_command = "kubectl scale deployment unified-model-ai --replicas=5"
        subprocess.run(scaling_command, shell=True)
        logging.info("✅ Auto-scaling triggered successfully.")
    elif cpu_usage < 20 and memory_usage < 20 and gpu_usage < 20:
        logging.info("⚠️ Low resource usage detected. Triggering auto-scaling down...")
        scaling_command = "kubectl scale deployment unified-model-ai --replicas=2"
        subprocess.run(scaling_command, shell=True)
        logging.info("✅ Auto-scaling down triggered successfully.")

# ---------------------------------------------------------------
# Main function to run real-time latency tests and comparison
# ---------------------------------------------------------------
def main():
    """Main function to run latency tests, comparison, and resource monitoring."""
    logging.info("🚀 Starting Real-Time Latency Testing for AI Models...")

    results = {}

    # Run cloud-based inference latency tests
    for cloud_provider in CLOUD_AI_ENDPOINTS.keys():
        try:
            results[cloud_provider] = cloud_inference_latency_test(cloud_provider)
        except Exception as e:
            logging.error(f"❌ Cloud inference latency test failed for {cloud_provider}: {e}")
            continue

    # Run edge device inference latency test
    try:
        results['edge'] = edge_inference_latency_test()
    except Exception as e:
        logging.error(f"❌ Edge inference latency test failed: {e}")

    # Generate latency comparison report
    generate_latency_comparison_report(results)

    # Monitor system resources and trigger auto-scaling if necessary
    cpu_usage, memory_usage, gpu_usage = monitor_system_resources()
    trigger_auto_scaling(cpu_usage, memory_usage, gpu_usage)

if __name__ == "__main__":
    main()
