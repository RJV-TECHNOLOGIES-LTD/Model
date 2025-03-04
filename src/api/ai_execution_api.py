from flask import Flask, jsonify, request
import torch

app = Flask(__name__)

@app.route('/execute', methods=['POST'])
def execute_model():
    data = request.json
    model_input = torch.tensor(data['input'])
    model_output = model_input * 2  # Placeholder for actual model execution
    return jsonify({"output": model_output.tolist()})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
