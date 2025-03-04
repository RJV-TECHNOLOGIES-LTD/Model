from transformers import pipeline

def generate_text(prompt):
    generator = pipeline("text-generation", model="gpt2")
    return generator(prompt, max_length=50, do_sample=True)

# Example Usage
if __name__ == '__main__':
    response = generate_text("The future of AI execution is")
    print(f"✔ LLM Output: {response[0]['generated_text']}")
