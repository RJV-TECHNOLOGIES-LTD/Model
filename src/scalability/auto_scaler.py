import os

def scale_execution(load):
    if load > 80:
        print("✔ Scaling up AI execution resources.")
    elif load < 30:
        print("✔ Scaling down AI execution resources.")
    else:
        print("✔ AI Execution is running optimally.")

# Example Usage
if __name__ == '__main__':
    scale_execution(85)
