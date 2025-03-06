from flask import Flask, request, jsonify
import logging
import os
from inference_mechanisms.inference_engine import InferenceEngine

# 🚀 Initialize Flask API
app = Flask(__name__)

# Set API-wide logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Default model configurations
MODEL_PATH = "memory_storage/checkpoint_epoch_10.h5"
MODEL_FORMAT = "h5"

# Ensure the model file exists
if not os.path.exists(MODEL_PATH):
    logging.error(f"Model file not found: {MODEL_PATH}")
    raise FileNotFoundError(f"Model file not found: {MODEL_PATH}")

# Load inference engine (Model verification occurs inside `InferenceEngine`)
try:
    inference_engine = InferenceEngine(model_format=MODEL_FORMAT, model_path=MODEL_PATH)
except Exception as e:
    logging.error(f"Failed to initialize inference engine: {e}")
    raise

@app.route("/infer", methods=["POST"])
def run_model():
    """
    API endpoint for running inference.

    Expected JSON Payload:
    {
        "input": [[...], [...], ...]  # 2D Array matching model input shape
    }

    Returns:
    {
        "result": [...],  # Model predictions
        "status": "success" | "error",
        "message": "..."  # Any relevant message
    }
    """
    data = request.get_json()
    if "input" not in data:
        return jsonify({"status": "error", "message": "Missing 'input' field in request"}), 400

    try:
        prediction = inference_engine.predict(data)
        return jsonify({"status": "success", "result": prediction.tolist()})
    except Exception as e:
        logging.error(f"Inference failed: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/health", methods=["GET"])
def health_check():
    """
    API endpoint for checking the health of the inference system.
    
    Returns:
    {
        "status": "ok",
        "message": "API is running"
    }
    """
    return jsonify({"status": "ok", "message": "API is running"}), 200

def start_api_server():
    """
    Start the REST API Server.
    """
    logging.info("Starting REST API Server...")
    app.run(host="0.0.0.0", port=5000)

if __name__ == "__main__":
    start_api_server()
