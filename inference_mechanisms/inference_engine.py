import torch
import logging

class InferenceEngine:
    def __init__(self, model):
        """Initialize inference engine."""
        self.model = model
        self.model.eval()
        logging.info("Inference engine initialized.")

    def predict(self, input_data):
        """Perform AI inference."""
        with torch.no_grad():
            input_tensor = input_data["example"].to("cuda" if torch.cuda.is_available() else "cpu")
            output = self.model(input_tensor)
            return output.cpu().numpy()
