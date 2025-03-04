import hashlib

def encrypt_model(model_data):
    return hashlib.sha256(model_data.encode()).hexdigest()

# Example Usage
if __name__ == '__main__':
    model_data = "NeuralNetworkModel"
    encrypted_data = encrypt_model(model_data)
    print(f"✔ Encrypted Model Data: {encrypted_data}")
