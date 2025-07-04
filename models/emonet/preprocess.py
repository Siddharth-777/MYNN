import torch
from torch.utils.data import Dataset
import pandas as pd
import json
from collections import defaultdict

class EmotionDataset(Dataset):
    def __init__(self, filepath, label_map, vocab=None, max_len=50):
        self.data = []
        self.label_map = label_map
        self.max_len = max_len
        self.vocab = vocab or defaultdict(lambda: len(self.vocab))  # auto-id

        df = pd.read_csv(filepath)  # header: text,label

        for _, row in df.iterrows():
            text = row["text"]
            label = row["label"]

            if label not in label_map:
                continue

            encoded = self.encode(text)
            label_idx = label_map[label]
            self.data.append((encoded, label_idx))

        self.vocab_size = len(self.vocab)

    def encode(self, text):
        tokens = text.lower().split()
        token_ids = [self.vocab[token] for token in tokens[:self.max_len]]
        if len(token_ids) < self.max_len:
            token_ids += [0] * (self.max_len - len(token_ids))
        return torch.tensor(token_ids, dtype=torch.long)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        return self.data[idx]

    def save_vocab(self, path):
        with open(path, "w") as f:
            json.dump(dict(self.vocab), f)

# === UTILS ===

def load_vocab(path):
    with open(path, "r") as f:
        vocab = json.load(f)
    vocab = defaultdict(lambda: 0, {k: int(v) for k, v in vocab.items()})
    return vocab

def load_label_map(path):
    with open(path, "r") as f:
        return json.load(f)

def encode_text(text, vocab, max_len=50):
    tokens = text.lower().split()
    token_ids = [vocab.get(token, 0) for token in tokens[:max_len]]
    if len(token_ids) < max_len:
        token_ids += [0] * (max_len - len(token_ids))
    return torch.tensor(token_ids, dtype=torch.long).unsqueeze(0)
