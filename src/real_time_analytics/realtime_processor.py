import time
import random

def stream_real_time_data():
    while True:
        data = {"timestamp": time.time(), "value": random.random()}
        print(f"✔ Real-Time Data: {data}")
        time.sleep(1)

# Example Usage
if __name__ == '__main__':
    stream_real_time_data()
