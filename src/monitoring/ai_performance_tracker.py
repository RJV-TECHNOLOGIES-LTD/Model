import psutil
import GPUtil

def track_performance():
    cpu_usage = psutil.cpu_percent(interval=1)
    ram_usage = psutil.virtual_memory().percent
    gpus = GPUtil.getGPUs()
    gpu_usage = [{"id": gpu.id, "load": gpu.load*100} for gpu in gpus] if gpus else "No GPU detected"

    return {"CPU": cpu_usage, "RAM": ram_usage, "GPU": gpu_usage}

# Example Usage
if __name__ == '__main__':
    performance_metrics = track_performance()
    print(f"✔ AI Performance Metrics: {performance_metrics}")
