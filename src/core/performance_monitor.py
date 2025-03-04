"""
Φ(a)-Optimized AI Execution Dashboard
-------------------------------------
Live AI execution monitoring with real-time performance tracking.
"""

import time
import psutil
import GPUtil

def monitor_performance():
    """Monitors AI execution performance in real-time."""
    print("🔍 Monitoring AI execution... (Press Ctrl+C to stop)")

    try:
        while True:
            cpu_usage = psutil.cpu_percent(interval=1)
            ram_usage = psutil.virtual_memory().percent
            gpus = GPUtil.getGPUs()
            gpu_usage = [{"id": gpu.id, "load": gpu.load*100} for gpu in gpus] if gpus else "No GPU detected"

            print(f"CPU: {cpu_usage}% | RAM: {ram_usage}% | GPU Usage: {gpu_usage}")
            time.sleep(2)
    except KeyboardInterrupt:
        print("🔴 Monitoring stopped.")

if __name__ == "__main__":
    monitor_performance()
