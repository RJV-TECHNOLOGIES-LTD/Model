import unittest
import torch
from src.core.ai_execution_engine import PhiAExecutionEngine

class TestAIExecutionEngine(unittest.TestCase):
    def setUp(self):
        self.engine = PhiAExecutionEngine()
    
    def test_device_detection(self):
        device = self.engine.auto_detect_device()
        self.assertIn(device, ["cpu", "cuda", "mps"])
    
    def test_model_loading(self):
        model = torch.nn.Linear(1024, 512)
        self.engine.load_model(model)
        self.assertIsNotNone(self.engine.model)

if __name__ == '__main__':
    unittest.main()
