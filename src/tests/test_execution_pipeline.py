import unittest
import torch
from src.optimization.ai_execution_optimizer import optimize_execution

class TestAIExecution(unittest.TestCase):
    def test_execution(self):
        model = torch.nn.Linear(1024, 512)
        input_data = torch.randn(1, 1024)
        output = optimize_execution(model, input_data)
        self.assertEqual(output.shape, torch.Size([1, 512]))

if __name__ == '__main__':
    unittest.main()
