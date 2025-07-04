import torch
import pandas as pd
from torch.utils.data import Dataset
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
import joblib

class ControllerDataset(Dataset):
    def __init__(self, csv_file):
        self.df = pd.read_csv(csv_file)
        self.vectorizer = TfidfVectorizer(max_features=128)
        self.encoder = LabelEncoder()

        self.X = self.vectorizer.fit_transform(self.df['query']).toarray()
        self.y = self.encoder.fit_transform(self.df['label'])

        joblib.dump(self.vectorizer, "vectorizer.pkl")
        joblib.dump(self.encoder, "label_encoder.pkl")

    def __len__(self):
        return len(self.y)

    def __getitem__(self, idx):
        return torch.tensor(self.X[idx], dtype=torch.float32), torch.tensor(self.y[idx], dtype=torch.long)
