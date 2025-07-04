import torch
import joblib
from models.mycelium_controller.controller import ControllerNet

vectorizer = joblib.load("models/mycelium_controller/vectorizer.pkl")
encoder = joblib.load("models/mycelium_controller/label_encoder.pkl")


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = ControllerNet(num_classes=4).to(device)
model.load_state_dict(torch.load("models/mycelium_controller/controller_model.pt", map_location=device))
model.eval()

while True:
    query = input("🔍 Enter query (or 'exit'): ")
    if query.lower() == 'exit':
        break
    x = vectorizer.transform([query]).toarray()
    x = torch.tensor(x, dtype=torch.float32).to(device)
    with torch.no_grad():
        out = model(x)
        pred = torch.argmax(out, dim=1)
        label = encoder.inverse_transform(pred.cpu())[0]
        print(f"🧠 Route to: {label}")
