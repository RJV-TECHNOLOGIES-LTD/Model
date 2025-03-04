import torch
import time

def execute_model(input_data):
    start_time = time.time()
    model = load_model("Phi-a-Optimized")
    output = model(input_data)
    execution_time = time.time() - start_time
    log_execution(output, execution_time)
    return output

def load_model(model_name):
    print(f"Loading model {model_name} with GPU acceleration: {torch.cuda.is_available()}")
    model = torch.load(f"models/{model_name}.pth")
    model.eval()
    return model

def log_execution(output, execution_time):
    with open("logs/execution.log", "a") as log_file:
        log_file.write(f"Execution completed in {execution_time} seconds.\nOutput: {output}\n")
