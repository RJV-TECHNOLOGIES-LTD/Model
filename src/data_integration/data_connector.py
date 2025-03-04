import pandas as pd

def load_data(source):
    if source.endswith(".csv"):
        return pd.read_csv(source)
    elif source.endswith(".json"):
        return pd.read_json(source)
    else:
        raise ValueError("Unsupported data format")

# Example Usage
if __name__ == '__main__':
    data = load_data('data/sample.csv')
    print("✔ Data Loaded Successfully")
