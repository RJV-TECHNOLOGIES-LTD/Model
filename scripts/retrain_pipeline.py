import os
import subprocess

def retrain_model():
    print("Starting model retraining...")
    subprocess.run(["python", "train.py", "--data", "data/new", "--output", "model_v2.pkl"])
    print("Model retraining completed.")

if __name__ == "__main__":
    retrain_model()
