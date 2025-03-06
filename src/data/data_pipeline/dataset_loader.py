import pandas as pd
import torch
import logging

class DataLoader:
    def __init__(self, dataset_path):
        """
        Initialize data loader.

        :param dataset_path: Path to dataset file.
        """
        self.dataset_path = dataset_path

    def load_data(self, batch_size=32):
        """
        Load dataset and return a DataLoader instance.

        :param batch_size: Batch size for training.
        :return: PyTorch DataLoader instance.
        """
        try:
            df = pd.read_parquet(self.dataset_path)
            inputs = torch.tensor(df.iloc[:, :-1].values, dtype=torch.float32)
            targets = torch.tensor(df.iloc[:, -1].values, dtype=torch.float32)
            dataset = torch.utils.data.TensorDataset(inputs, targets)
            return torch.utils.data.DataLoader(dataset, batch_size=batch_size, shuffle=True)
        except Exception as e:
            logging.error(f"Dataset loading failed: {e}")
            raise
