from memory_storage.model_checkpoints import ModelCheckpointManager

class InferenceEngine:
    def __init__(self, model_format, model_path):
        """
        Initialize inference engine with FAISS vector memory.

        :param model_format: Format of the model (h5, onnx, tflite).
        :param model_path: Path to the model file.
        """
        self.model_format = model_format
        self.model_path = model_path
        self.model_checkpoint_manager = ModelCheckpointManager()

        # Verify model integrity before loading
        checkpoint_name = os.path.basename(self.model_path)
        if not self.verify_signature(checkpoint_name):
            logging.error("Model integrity verification failed. Aborting inference.")
            raise ValueError("Model integrity verification failed. The model may be corrupted.")

        self.model = self.load_model()

    def search_similar_models(self, query_embedding, k=3):
        """
        Find the nearest trained models using FAISS vector memory.

        :param query_embedding: Query vector for similarity search.
        :param k: Number of nearest models to retrieve.
        :return: Nearest model indices.
        """
        indices, distances = self.model_checkpoint_manager.search_similar_models(query_embedding, k)
        logging.info(f"Found similar models: {indices}")
        return indices, distances
