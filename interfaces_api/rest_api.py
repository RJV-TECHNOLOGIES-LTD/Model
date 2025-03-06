from flask import Flask, request, jsonify
import logging
import grpc
import os
import xml.etree.ElementTree as ET
import interfaces_api.grpc_service_pb2 as pb2
import interfaces_api.grpc_service_pb2_grpc as pb2_grpc

# 🚀 Initialize Flask API
app = Flask(__name__)

# Set API-wide logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# gRPC Connection
channel = grpc.insecure_channel("localhost:50051")
grpc_stub = pb2_grpc.InferenceServiceStub(channel)

# Load API Schema from `api_schema.xml`
def load_api_schema():
    """
    Load and parse the API schema.
    """
    schema_path = "interfaces_api/api_schema.xml"
    if not os.path.exists(schema_path):
        logging.error(f"API Schema file not found: {schema_path}")
        raise FileNotFoundError(f"API Schema file not found: {schema_path}")

    try:
        tree = ET.parse(schema_path)
        root = tree.getroot()
        schema = {child.tag: child.text for child in root}
        return schema
    except Exception as e:
        logging.error(f"Failed to load API Schema: {e}")
        raise

API_SCHEMA = load_api_schema()

@app.route("/infer", methods=["POST"])
def run_model():
    """
    API endpoint for running inference with schema validation.

    Expected JSON Payload:
    {
        "input": [0.1, 0.2, 0.3, 0.4]  # Array matching model input shape
    }

    Returns:
    {
        "result": [...],  # Model predictions
        "status": "success" | "error",
        "message": "..."  # Any relevant message
    }
    """
    data = request.get_json()

    # Validate input using API schema
    if "input" not in data:
        return jsonify({"status": "error", "message": "Missing 'input' field"}), 400

    if not isinstance(data["input"], list):
        return jsonify({"status": "error", "message": "Invalid input format. Expected an array."}), 400

    try:
        # Convert input to gRPC format
        grpc_request = pb2.InferenceRequest(input=data["input"])
        grpc_response = grpc_stub.RunInference(grpc_request)

        return jsonify({
            "status": grpc_response.status,
            "result": grpc_response.result,
            "message": grpc_response.message
        })
    except Exception as e:
        logging.error(f"Inference failed: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/health", methods=["GET"])
def health_check():
    """
    API endpoint for checking the health of the REST and gRPC inference system.
    
    Returns:
    {
        "status": "ok",
        "message": "API is running"
    }
    """
    grpc_health_request = pb2.HealthRequest()
    grpc_health_response = grpc_stub.HealthCheck(grpc_health_request)

    return jsonify({"status": grpc_health_response.status, "message": grpc_health_response.message}), 200

def start_api_server():
    """
    Start the REST API Server.
    """
    logging.info("Starting REST API Server...")
    app.run(host="0.0.0.0", port=5000)

if __name__ == "__main__":
    start_api_server()
