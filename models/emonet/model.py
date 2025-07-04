import torch
import torch.nn as nn

class EmoNet(nn.Module):
    def __init__(self, vocab_size, num_classes, embed_dim=100, hidden_dim=128):
        super(EmoNet, self).__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim)
        self.fc1 = nn.Linear(embed_dim, hidden_dim)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_dim, num_classes)

    def forward(self, x):
        x = self.embedding(x)                      # (B, T, E)
        x = x.mean(dim=1)                          # average pooling (B, E)
        x = self.relu(self.fc1(x))                 # (B, H)
        return self.fc2(x)                         # (B, num_classes)
