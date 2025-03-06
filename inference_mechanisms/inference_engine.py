import torch
import onnxruntime
import tensorflow.lite as tflite
import logging
import os

class InferenceEngine:
    def __init__(self, model_format, model_path):
        """
        Initialize inference engine and load the model.

        :param model_format: Format of the model (h5, onnx, tflite)
        :param model_path: Path to the model file.
        """
        self.model_format = model_format
        self.model_path = model_path
        self.model = self.load_model()

    def load_model(self):
        """
        Load the AI model from the correct format.
        """
        if not os.path.exists(self.model_path):
            logging.error(f"Model file not found: {self.model_path}")
            raise FileNotFoundError(f"Model file not found: {self.model_path}")

        try:
            if self.model_format == "h5":
                model = torch.load(self.model_path, map_location="cuda" if torch.cuda.is_available() else "cpu")
                logging.info(f"Loaded PyTorch model from {self.model_path}")
            elif self.model_format == "onnx":
                model = onnxruntime.InferenceSession(self.model_path)
                logging.info(f"Loaded ONNX model from {self.model_path}")
            elif self.model_format == "tflite":
                interpreter = tflite.Interpreter(model_path=self.model_path)
                interpreter.allocate_tensors()
                model = interpreter
                logging.info(f"Loaded TensorFlow Lite model from {self.model_path}")
            else:
                raise ValueError(f"Unsupported model format: {self.model_format}")

            return model
        except Exception as e:
            logging.error(f"Failed to load model: {e}")
            raise

    def predict(self, input_data):
        """
        Perform inference using the loaded model.

        :param input_data: Dictionary containing input tensor.
        :return: Model prediction.
        """
        try:
            if self.model_format == "h5":
                input_tensor = torch.tensor(input_data["input"]).to("cuda" if torch.cuda.is_available() else "cpu")
                output = self.model(input_tensor).cpu().numpy()
            elif self.model_format == "onnx":
                input_tensor = {self.model.get_inputs()[0].name: input_data["input"]}
                output = self.model.run(None, input_tensor)[0]
            elif self.model_format == "tflite":
                input_tensor = input_data["input"]
                input_details = self.model.get_input_details()
                output_details = self.model.get_output_details()
                self.model.set_tensor(input_details[0]['index'], input_tensor)
                self.model.invoke()
                output = self.model.get_tensor(output_details[0]['index'])
            else:
                raise ValueError(f"Unsupported model format: {self.model_format}")

            return output
        except Exception as e:
            logging.error(f"Inference failed: {e}")
            raise
