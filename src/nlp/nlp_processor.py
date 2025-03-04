import spacy

nlp = spacy.load("en_core_web_sm")

def process_text(text):
    doc = nlp(text)
    return [(token.text, token.pos_) for token in doc]

# Example Usage
if __name__ == '__main__':
    text_analysis = process_text("AI execution optimization is advancing rapidly.")
    print(f"✔ NLP Analysis: {text_analysis}")
