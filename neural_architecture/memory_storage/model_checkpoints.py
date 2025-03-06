import faiss
import numpy as np
import os
import logging
import torch

class ModelCheckpointManager:
    def __init__(self, checkpoint_dir="memory_storage/", vector_memory_path="memory_storage/vector_memory.faiss", dim=512):
        """
        Initialize model checkpoint manager with FAISS-based vector memory.

        :param checkpoint_dir: Directory where model checkpoints are stored.
        :param vector_memory_path: Path to FAISS index file.
        :param dim: Dimension of vectors to be stored (default: 512).
        """
        self.checkpoint_dir = checkpoint_dir
        self.vector_memory_path = vector_memory_path
        self.dim = dim
        self.index = None

        # Ensure storage directory exists
        os.makedirs(self.checkpoint_dir, exist_ok=True)

        # Load or create FAISS index
        if os.path.exists(self.vector_memory_path):
            self.load_faiss_index()
        else:
            self.create_faiss_index()

    def create_faiss_index(self):
        """
        Create a new FAISS index for vector storage.
        """
        self.index = faiss.IndexFlatL2(self.dim)  # L2 distance for similarity search
        logging.info("Created new FAISS vector memory index.")

    def load_faiss_index(self):
        """
        Load existing FAISS index from file.
        """
        try:
            self.index = faiss.read_index(self.vector_memory_path)
            logging.info(f"Loaded FAISS vector memory from {self.vector_memory_path}.")
        except Exception as e:
            logging.error(f"Failed to load FAISS vector memory: {e}")
            self.create_faiss_index()

    def save_faiss_index(self):
        """
        Save FAISS index to file.
        """
        try:
            faiss.write_index(self.index, self.vector_memory_path)
            logging.info(f"Saved FAISS vector memory to {self.vector_memory_path}.")
        except Exception as e:
            logging.error(f"Failed to save FAISS vector memory: {e}")

    def save_model_checkpoint(self, model, model_id):
        """
        Save model checkpoint and add its embedding to FAISS.

        :param model: Trained model instance.
        :param model_id: Unique model identifier.
        """
        checkpoint_path = os.path.join(self.checkpoint_dir, f"model_{model_id}.h5")

        try:
            # Save model state
            torch.save(model.state_dict(), checkpoint_path)
            logging.info(f"Saved model checkpoint: {checkpoint_path}")

            # Generate and store model embedding in FAISS
            embedding = model.get_embedding().detach().cpu().numpy().reshape(1, -1)  # Example
            self.index.add(embedding)
            self.save_faiss_index()

            logging.info(f"Stored model embedding for model ID: {model_id} in FAISS.")
        except Exception as e:
            logging.error(f"Failed to save model checkpoint and embedding: {e}")

    def search_similar_models(self, query_embedding, k=5):
        """
        Find the nearest trained models using FAISS vector memory.

        :param query_embedding: Query vector for similarity search.
        :param k: Number of nearest models to retrieve.
        :return: Nearest model indices.
        """
        if not isinstance(query_embedding, np.ndarray):
            query_embedding = np.array(query_embedding).astype("float32")

        query_embedding = query_embedding.reshape(1, -1)  # Ensure correct shape
        distances, indices = self.index.search(query_embedding, k)
        return indices[0], distances[0]

