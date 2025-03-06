from memory_storage.model_checkpoints import ModelCheckpointManager

class Trainer:
    def __init__(self, model, dataset_path):
        """
        Initialize trainer with model, dataset, checkpoint manager, and FAISS indexing.
        """
        self.model = model
        self.dataset_path = dataset_path
        self.checkpoint_manager = ModelCheckpointManager()

    def train(self):
        """
        Train model, save checkpoints, and index embeddings in FAISS.
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

            # Save model checkpoint and update FAISS
            model_id = f"epoch_{epoch}"
            self.checkpoint_manager.save_model_checkpoint(self.model, model_id)


