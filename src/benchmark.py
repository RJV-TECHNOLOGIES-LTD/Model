import torch
import time
from model_conversion import convert_model

# Define test AI model
class TestModel(torch.nn.Module):
    def __init__(self, input_dim, output_dim):
        super(TestModel, self).__init__()
        self.fc = torch.nn.Linear(input_dim, output_dim)
    
    def forward(self, x):
        return self.fc(x)

# Benchmark function
def benchmark_model(model, test_input):
    start_time = time.time()
    for _ in range(100):  # Run 100 inference cycles
        _ = model(test_input)
    return time.time() - start_time

# Setup model
test_input = torch.randn(1, 1024)
standard_model = TestModel(1024, 512)
converted_model = convert_model(standard_model)

# Run benchmark
standard_time = benchmark_model(standard_model, test_input)
converted_time = benchmark_model(converted_model, test_input)

# Print results
print(f"Standard Model Execution Time: {standard_time:.6f} sec")
print(f"Φ(a)-Optimized Model Execution Time: {converted_time:.6f} sec")
print(f"Speed Improvement: {standard_time / converted_time:.2f}x")
