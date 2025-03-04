import pandas as pd

def validate_data(file_path):
    data = pd.read_csv(file_path)
    if data.isnull().sum().sum() > 0:
        raise ValueError("Data contains missing values!")
    if data.duplicated().sum() > 0:
        raise ValueError("Data contains duplicate records!")
    if (data < 0).sum().sum() > 0:
        raise ValueError("Data contains negative values where not expected!")
    print("Data validation passed.")

if __name__ == "__main__":
    validate_data("data/new_data.csv")
