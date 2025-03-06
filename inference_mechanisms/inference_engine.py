import hashlib
import os

class InferenceEngine:
    def __init__(self, model_format, model_path):
        """
        Initialize inference engine and verify model integrity.

        :param model_format: Format of the model (h5, onnx, tflite).
        :param model_path: Path to the model file.
        """
        self.model_format = model_format
        self.model_path = model_path
        self.signature_path = os.path.join("security_integrity", "model_verification.sig")

        # Verify model integrity before loading
        checkpoint_name = os.path.basename(self.model_path)
        if not self.verify_signature(checkpoint_name):
            logging.error("Model integrity verification failed. Aborting inference.")
            raise ValueError("Model integrity verification failed. The model may be corrupted.")

        self.model = self.load_model()

    def verify_signature(self, checkpoint_name):
        """
        Verify the integrity of a model checkpoint using SHA256.

        :param checkpoint_name: Filename of the checkpoint.
        :return: Boolean indicating whether the model is valid.
        """
        checkpoint_path = os.path.join("memory_storage", checkpoint_name)
        if not os.path.exists(checkpoint_path):
            logging.error(f"Checkpoint not found for verification: {checkpoint_path}")
            raise FileNotFoundError(f"Checkpoint not found: {checkpoint_path}")

        if not os.path.exists(self.signature_path):
            logging.error("Signature file missing. Cannot verify model integrity.")
            return False

        try:
            with open(checkpoint_path, "rb") as file:
                model_hash = hashlib.sha256(file.read()).hexdigest()

            with open(self.signature_path, "r") as sig_file:
                stored_hash = sig_file.read().strip()

            if model_hash == stored_hash:
                logging.info("Model integrity verified successfully.")
                return True
            else:
                logging.error("Model integrity check failed. The model file may have been altered.")
                return False
        except Exception as e:
            logging.error(f"Model verification failed: {e}")
            return False
