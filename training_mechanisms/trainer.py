import hashlib
import os

class Trainer:
    def __init__(self, model, dataset_path):
        """
        Initialize trainer with model, dataset, and checkpoint manager.
        """
        self.model = model
        self.dataset_path = dataset_path
        self.checkpoint_manager = ModelCheckpointManager()
        self.signature_path = os.path.join("security_integrity", "model_verification.sig")

    def generate_signature(self, checkpoint_name):
        """
        Generate SHA256 signature for a model checkpoint.
        
        :param checkpoint_name: Filename of the checkpoint.
        """
        checkpoint_path = os.path.join(self.checkpoint_manager.checkpoint_dir, checkpoint_name)
        if not os.path.exists(checkpoint_path):
            logging.error(f"Checkpoint not found for signing: {checkpoint_path}")
            raise FileNotFoundError(f"Checkpoint not found: {checkpoint_path}")

        try:
            with open(checkpoint_path, "rb") as file:
                model_hash = hashlib.sha256(file.read()).hexdigest()

            with open(self.signature_path, "w") as sig_file:
                sig_file.write(model_hash)

            logging.info(f"Generated model signature: {model_hash}")
        except Exception as e:
            logging.error(f"Failed to generate model signature: {e}")
            raise

    def train(self):
        """
        Train model, save checkpoints, and generate verification signature.
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
            checkpoint_name = f"checkpoint_epoch_{epoch}.h5"
            self.checkpoint_manager.save_model(self.model, epoch)
            
            # Generate model signature
            self.generate_signature(checkpoint_name)

