import torch
import torch.nn as nn
import torch.optim as optim
import xml.etree.ElementTree as ET
import yaml
import logging
from training_mechanisms.loss_functions import compute_loss
from data_pipeline.dataset_loader import DataLoader
from memory_storage.model_checkpoints import ModelCheckpointManager

def load_training_config():
    """
    Load training settings from `training_config.xml`.
    """
    try:
        tree = ET.parse("training_mechanisms/training_config.xml")
        root = tree.getroot()
        config = {
            "epochs": int(root.find("epochs").text),
            "batch_size": int(root.find("batch_size").text),
            "learning_rate": float(root.find("learning_rate").text)
        }
        return config
    except Exception as e:
        logging.error(f"Failed to load training configuration: {e}")
        raise

def load_optimizer_config():
    """
    Load optimizer settings from `optimization_algorithms.yaml`.
    """
    try:
        with open("training_mechanisms/optimization_algorithms.yaml", "r") as file:
            config = yaml.safe_load(file)
        return config
    except Exception as e:
        logging.error(f"Failed to load optimizer settings: {e}")
        raise

class Trainer:
    def __init__(self, model, dataset_path):
        """
        Initialize trainer with model, dataset, and checkpoint manager.
        Training parameters are loaded dynamically from `training_config.xml`.
        """
        self.model = model
        self.dataset_path = dataset_path
        self.config = load_training_config()
        self.optimizer_config = load_optimizer_config()
        self.dataloader = DataLoader(self.dataset_path).load_data(batch_size=self.config["batch_size"])
        self.criterion = compute_loss
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.checkpoint_manager = ModelCheckpointManager()
        self.model.to(self.device)

        # Set up optimizer based on configuration
        if self.optimizer_config["optimizer"] == "adam":
            self.optimizer = optim.Adam(self.model.parameters(), lr=self.config["learning_rate"])
        elif self.optimizer_config["optimizer"] == "sgd":
            self.optimizer = optim.SGD(self.model.parameters(), lr=self.config["learning_rate"], momentum=0.9)
        else:
            raise ValueError(f"Unsupported optimizer: {self.optimizer_config['optimizer']}")

    def train(self):
        """
        Train model using parameters defined in `training_config.xml`.
        Save checkpoints at each epoch.
        """
        epochs = self.config["epochs"]
        self.model.train()
        for epoch in range(epochs):
            for batch in self.dataloader:
                inputs, targets = batch["input"].to(self.device), batch["target"].to(self.device)
                self.optimizer.zero_grad()
                outputs = self.model(inputs)
                loss = self.criterion(outputs, targets)
                loss.backward()
                self.optimizer.step()
            logging.info(f"Epoch {epoch + 1}/{epochs} - Loss: {loss.item()}")

            # Save model checkpoint
            self.checkpoint_manager.save_model(self.model, epoch)
