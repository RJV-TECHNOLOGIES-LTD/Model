import torch
import os
import logging

class ModelCheckpointManager:
    def __init__(self, checkpoint_dir="memory_storage/"):
        """Initialize checkpoint manager."""
        self.checkpoint_dir = checkpoint_dir
        os.makedirs(self.checkpoint_dir, exist_ok=True)

    def save_model(self, model, epoch):
        """Save model checkpoint."""
        checkpoint_path = os.path.join(self.checkpoint_dir, f"checkpoint_epoch_{epoch}.h5")
        torch.save(model.state_dict(), checkpoint_path)
        logging.info(f"Model checkpoint saved: {checkpoint_path}")

    def load_model(self, model_path):
        """Load AI model from checkpoint."""
        if not os.path.exists(model_path):
            logging.error(f"Model checkpoint not found: {model_path}")
            return None
        model = torch.load(model_path, map_location="cuda" if torch.cuda.is_available() else "cpu")
        logging.info(f"Model loaded from {model_path}")
        return model
