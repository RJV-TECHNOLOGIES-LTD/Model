import faiss
import numpy as np
import os
import logging

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

    def add_model_embedding(self, model_embedding):
        """
        Add a model embedding to the FAISS index.

        :param model_embedding: The embedding vector of the model.
        """
        if not isinstance(model_embedding, np.ndarray):
            model_embedding = np.array(model_embedding).astype("float32")

        if model_embedding.shape[1] != self.dim:
            raise ValueError(f"Expected vector dimension {self.dim}, got {model_embedding.shape[1]}.")

        self.index.add(model_embedding)
        self.save_faiss_index()
        logging.info(f"Added model embedding to FAISS vector memory.")

    def search_similar_models(self, query_embedding, k=5):
        """
        Search for the nearest similar models based on embedding similarity.

        :param query_embedding: Query vector for searching similar models.
        :param k: Number of nearest models to retrieve.
        :return: List of nearest model indices and distances.
        """
        if not isinstance(query_embedding, np.ndarray):
            query_embedding = np.array(query_embedding).astype("float32")

        query_embedding = query_embedding.reshape(1, -1)  # Ensure correct shape
        distances, indices = self.index.search(query_embedding, k)
        return indices[0], distances[0]
