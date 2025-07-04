import torch
import torch.nn as nn
import torch.nn.functional as F

class ControllerNet(nn.Module):
    def __init__(self, input_dim=68, hidden_dim=64, num_classes=4):
        super(ControllerNet, self).__init__()
        self.fc1 = nn.Linear(input_dim, hidden_dim)
        self.fc2 = nn.Linear(hidden_dim, num_classes)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        return self.fc2(x)
