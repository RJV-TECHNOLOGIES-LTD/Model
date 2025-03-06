import torch
import torch.nn as nn
import torch.optim as optim
import logging
from training_mechanisms.loss_functions import compute_loss
from training_mechanisms.optimization_algorithms import get_optimizer
from data_pipeline.dataset_loader import DataLoader

class Trainer:
    def __init__(self, model, dataset_path, checkpoint_manager):
        """Initialize trainer with model, dataset, and checkpoint manager."""
        self.model = model
        self.dataset_path = dataset_path
        self.dataloader = DataLoader(self.dataset_path).load_data()
        self.optimizer = get_optimizer(self.model)
        self.criterion = compute_loss
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.checkpoint_manager = checkpoint_manager
        self.model.to(self.device)

    def train(self, epochs=10):
        """Train model and save checkpoints."""
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
            self.checkpoint_manager.save_model(self.model, epoch)
