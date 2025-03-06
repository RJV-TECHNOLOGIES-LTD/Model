import torch
import os
import logging

class ModelCheckpointManager:
    def __init__(self, checkpoint_dir="memory_storage/"):
        """
        Initialize the checkpoint manager.
        
        :param checkpoint_dir: Directory where checkpoints are stored.
        """
        self.checkpoint_dir = checkpoint_dir
        os.makedirs(self.checkpoint_dir, exist_ok=True)

    def save_model(self, model, epoch):
        """
        Save model checkpoint in `.h5` format.

        :param model: PyTorch model instance.
        :param epoch: Training epoch number.
        """
        checkpoint_path = os.path.join(self.checkpoint_dir, f"checkpoint_epoch_{epoch}.h5")
        try:
            torch.save(model.state_dict(), checkpoint_path)
            logging.info(f"Model checkpoint saved at: {checkpoint_path}")
        except Exception as e:
            logging.error(f"Failed to save model checkpoint: {e}")
            raise

    def load_model(self, model, checkpoint_name):
        """
        Load model checkpoint.

        :param model: PyTorch model instance.
        :param checkpoint_name: Filename of the checkpoint to load.
        :return: Model with loaded weights.
        """
        checkpoint_path = os.path.join(self.checkpoint_dir, checkpoint_name)
        if not os.path.exists(checkpoint_path):
            logging.error(f"Checkpoint not found: {checkpoint_path}")
            raise FileNotFoundError(f"Checkpoint not found: {checkpoint_path}")

        try:
            model.load_state_dict(torch.load(checkpoint_path, map_location="cuda" if torch.cuda.is_available() else "cpu"))
            logging.info(f"Loaded model checkpoint from {checkpoint_path}")
            return model
        except Exception as e:
            logging.error(f"Failed to load model checkpoint: {e}")
            raise
