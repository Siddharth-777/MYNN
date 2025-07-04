import torch
import pandas as pd
import pickle
from cortex import CortexFusion

# Load model and vectorizer
with open("vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

model = CortexFusion(input_dim=len(vectorizer.get_feature_names_out()))
model.load_state_dict(torch.load("cortex_model.pt", map_location=torch.device("cpu")))
model.eval()

# Load original CSV for index lookup
df = pd.read_csv("data.csv")

# Interactive test
while True:
    print("\n🤖 Enter input features:")
    logic = input("LogicNet → ")
    memory = input("MemoryNet → ")
    creative = input("CreativeNet → ")
    emotion = input("EmoNet → ")

    combined = " ".join([logic, memory, creative, emotion])
    vec = vectorizer.transform([combined]).toarray()
    x = torch.tensor(vec, dtype=torch.float32)

    with torch.no_grad():
        prediction = model(x).item()
        idx = int(round(prediction))

        if 0 <= idx < len(df):
            print(f"\n🧠 Final Response:\n{df.iloc[idx]['final_response']}")
        else:
            print("⚠️ Out-of-range prediction.")
