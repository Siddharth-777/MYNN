import torch
import torch.nn as nn
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from cortex import CortexFusion
import pickle

# Load dataset
df = pd.read_csv("data.csv")

# Inputs: each of the 4 component outputs
X_text = df[["logicnet_output", "memorynet_chunks", "creativenet_output", "emonet_emotion"]].astype(str)
y = list(range(len(df)))  # target is the row index

# Flatten all strings and encode as text
all_text = X_text.apply(lambda row: " ".join(row.values), axis=1)

# Vectorize
vectorizer = TfidfVectorizer()
X_vec = vectorizer.fit_transform(all_text).toarray()

# Save vectorizer
with open("vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X_vec, y, test_size=0.2, random_state=42)

# Torch tensors
X_train = torch.tensor(X_train, dtype=torch.float32)
y_train = torch.tensor(y_train, dtype=torch.float32)

# Model
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = CortexFusion(input_dim=X_train.shape[1]).to(device)

criterion = nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

# Training
EPOCHS = 15
for epoch in range(EPOCHS):
    model.train()
    optimizer.zero_grad()
    output = model(X_train.to(device)).squeeze()
    loss = criterion(output, y_train.to(device))
    loss.backward()
    optimizer.step()
    print(f"Epoch {epoch+1} | Loss: {loss.item():.4f}")

torch.save(model.state_dict(), "cortex_model.pt")
print("✅ Model saved to cortex_model.pt")
