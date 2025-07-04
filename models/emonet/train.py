import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from preprocess import EmotionDataset, load_label_map
from model import EmoNet

# === HYPERPARAMETERS ===
BATCH_SIZE = 32
EPOCHS = 15
LR = 0.001

# === LOAD LABELS + DATASET ===
label_map = load_label_map("emotions.json")
dataset = EmotionDataset("data/goemotions_real_clean.csv", label_map)
train_loader = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=True)

# === INIT MODEL ===
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = EmoNet(vocab_size=dataset.vocab_size, num_classes=len(label_map)).to(device)

criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=LR)

# === TRAIN LOOP ===
for epoch in range(EPOCHS):
    model.train()
    total_loss = 0
    correct = 0
    total = 0

    for inputs, targets in train_loader:
        inputs, targets = inputs.to(device), targets.to(device)

        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, targets)
        loss.backward()
        optimizer.step()

        total_loss += loss.item()
        _, predicted = torch.max(outputs, 1)
        correct += (predicted == targets).sum().item()
        total += targets.size(0)

    acc = correct / total
    print(f"Epoch {epoch+1}/{EPOCHS} | Loss: {total_loss:.4f} | Accuracy: {acc:.4f}")

# === SAVE ===
torch.save(model.state_dict(), "emonet_model.pt")
dataset.save_vocab("vocab.json")
print("✅ Model and vocab saved.")
