import torch
from model import EmoNet
from preprocess import encode_text, load_vocab, load_label_map

# === SETUP ===
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
label_map = load_label_map("emotions.json")
idx_to_label = {v: k for k, v in label_map.items()}
vocab = load_vocab("vocab.json")

model = EmoNet(vocab_size=len(vocab), num_classes=len(label_map))
model.load_state_dict(torch.load("emonet_model.pt", map_location=device))
model.to(device)
model.eval()

# === INTERACTIVE ===
while True:
    text = input("😶 Enter text (or 'exit'): ")
    if text.lower() == "exit":
        break

    with torch.no_grad():
        encoded = encode_text(text, vocab).to(device)
        output = model(encoded)
        probs = torch.softmax(output, dim=1)
        top_prob, top_idx = torch.max(probs, 1)

        emotion = idx_to_label[top_idx.item()]
        confidence = top_prob.item()
        print(f"🧠 Emotion: {emotion} (confidence: {confidence:.2f})\n")
