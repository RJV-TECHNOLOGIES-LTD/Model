import time

def benchmark_model(model, test_data):
    start_time = time.time()
    predictions = model.predict(test_data)
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Model executed in {execution_time:.4f} seconds.")
    return execution_time

if __name__ == "__main__":
    from execution import load_model  # Assuming execution.py exists
    model = load_model("model_v2.pkl")
    test_data = [...]  # Placeholder for test dataset
    benchmark_model(model, test_data)
