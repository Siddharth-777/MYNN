import torch
import torch.nn as nn
import torch.nn.functional as F

class CortexFusion(nn.Module):
    def __init__(self, input_dim=4, hidden_dim=64):
        super(CortexFusion, self).__init__()
        self.fc1 = nn.Linear(input_dim, hidden_dim)
        self.fc2 = nn.Linear(hidden_dim, hidden_dim)
        self.fc3 = nn.Linear(hidden_dim, 1)  # output is a single value (index of final response row)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        return self.fc3(x)
