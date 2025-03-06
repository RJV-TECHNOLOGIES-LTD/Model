from flask import Flask, request, jsonify
import logging
import grpc
import os
import interfaces_api.grpc_service_pb2 as pb2
import interfaces_api.grpc_service_pb2_grpc as pb2_grpc

# 🚀 Initialize Flask API
app = Flask(__name__)

# Set API-wide logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# gRPC Connection
channel = grpc.insecure_channel("localhost:50051")
grpc_stub = pb2_grpc.InferenceServiceStub(channel)

@app.route("/infer", methods=["POST"])
def run_model():
    """
    API endpoint for running inference over both REST and gRPC.

    Expected JSON Payload:
    {
        "input": [[...], [...], ...]  # Input tensor array
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
 


if __name__ == "__main__":
    start_api_server()
