import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask import Flask, request, jsonify, render_template, redirect, url_for, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
from backend.utils.pdf_parser import extract_text_from_pdf
from models.emonet.model import EmoNet
from models.emonet.preprocess import encode_text, load_vocab, load_label_map
from models.creativenet.generate import generate_creative_associations
from models.logicnet.logic_qa import answer_query as logicnet_answer_query
from models.mycelium_controller.controller import ControllerNet
from models.memorynet.transformer_knowledge import query_transformer_knowledge
import joblib
import torch
import numpy as np
from models.cortex_fusion.generate_response import generate_response as cortex_fuse_response

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# === GLOBAL STATE (single user) ===
PDF_CHUNKS = []

# === Load Models/Resources ===
try:
    print("Loading EmoNet...")
    # EmoNet
    emonet_device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    emotion_label_map = load_label_map("models/emonet/emotions.json")
    emotion_idx_to_label = {v: k for k, v in emotion_label_map.items()}
    emotion_vocab = load_vocab("models/emonet/vocab.json")
    emotion_model = EmoNet(vocab_size=len(emotion_vocab), num_classes=len(emotion_label_map))
    emotion_model.load_state_dict(torch.load("models/emonet/emonet_model.pt", map_location=emonet_device))
    emotion_model.to(emonet_device)
    emotion_model.eval()
    print("✅ EmoNet loaded successfully")

    print("Loading Mycelium Controller...")
    # Mycelium Controller
    controller_vectorizer = joblib.load("models/mycelium_controller/vectorizer.pkl")
    controller_encoder = joblib.load("models/mycelium_controller/label_encoder.pkl")
    controller_model = ControllerNet(num_classes=4).to(emonet_device)
    controller_model.load_state_dict(torch.load("models/mycelium_controller/controller_model.pt", map_location=emonet_device))
    controller_model.eval()
    print("✅ Mycelium Controller loaded successfully")
    
    print("✅ All models loaded successfully!")
    
except Exception as e:
    print(f"❌ Error loading models: {e}")
    import traceback
    traceback.print_exc()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/models')
def models():
    return render_template('models.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/creator')
def creator():
    return render_template('creator.html')

@app.route('/analyze')
def analyze():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_pdf():
    global PDF_CHUNKS
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    try:
        PDF_CHUNKS = extract_text_from_pdf(filepath)
        return jsonify({'message': 'File processed', 'chunks': PDF_CHUNKS}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/ask', methods=['POST'])
def ask():
    global PDF_CHUNKS
    try:
        data = request.get_json()
        question = data.get('question', '')
        if not question:
            return jsonify({'error': 'No question provided'}), 400
        if not PDF_CHUNKS:
            return jsonify({'error': 'No PDF uploaded yet'}), 400

        print(f"Processing question: {question}")

        # --- Mycelium Controller: Route to model (optional, for info) ---
        try:
            print("Running Mycelium Controller...")
            x = controller_vectorizer.transform([question]).toarray()
            x = torch.tensor(x, dtype=torch.float32).to(emonet_device)
            with torch.no_grad():
                out = controller_model(x)
                pred = torch.argmax(out, dim=1)
                route_label = controller_encoder.inverse_transform(pred.cpu())[0]
            print(f"✅ Route: {route_label}")
        except Exception as e:
            print(f"❌ Mycelium Controller error: {e}")
            route_label = "unknown"

        # --- MemoryNet ---
        try:
            print("Running MemoryNet...")
            # Use Transformer knowledge base
            memorynet_results = query_transformer_knowledge(question, top_k=3)
            if memorynet_results:
                memorynet_chunks = [chunk for chunk, score in memorynet_results]
                memorynet_output = " ".join(memorynet_chunks)
            else:
                # Fallback to searching in uploaded PDF chunks
                if PDF_CHUNKS:
                    question_lower = question.lower()
                    relevant_chunks = []
                    for chunk in PDF_CHUNKS:
                        chunk_lower = chunk.lower()
                        # Simple relevance scoring based on word overlap
                        question_words = set(question_lower.split())
                        chunk_words = set(chunk_lower.split())
                        overlap = len(question_words.intersection(chunk_words))
                        if overlap > 0:
                            relevant_chunks.append((chunk, overlap))
                    
                    # Sort by relevance and take top 3
                    relevant_chunks.sort(key=lambda x: x[1], reverse=True)
                    if relevant_chunks:
                        memorynet_output = " ".join([chunk for chunk, score in relevant_chunks[:3]])
                    else:
                        memorynet_output = "No relevant information found in the uploaded document."
                else:
                    memorynet_output = "No relevant information found in the Transformer knowledge base."
            print("✅ MemoryNet completed")
        except Exception as e:
            print(f"❌ MemoryNet error: {e}")
            memorynet_output = "Memory retrieval failed"

        # --- LogicNet ---
        try:
            print("Running LogicNet...")
            logicnet_output = logicnet_answer_query(question, PDF_CHUNKS)
            print("✅ LogicNet completed")
        except Exception as e:
            print(f"❌ LogicNet error: {e}")
            logicnet_output = "Logical analysis failed"

        # --- CreativeNet ---
        try:
            print("Running CreativeNet...")
            creativenet_outputs = generate_creative_associations(question, top_k=1)
            creativenet_output = creativenet_outputs[0] if creativenet_outputs else ""
            print("✅ CreativeNet completed")
        except Exception as e:
            print(f"❌ CreativeNet error: {e}")
            creativenet_output = "Creative generation failed"

        # --- EmoNet ---
        try:
            print("Running EmoNet...")
            with torch.no_grad():
                encoded = encode_text(question, emotion_vocab).to(emonet_device)
                output = emotion_model(encoded)
                probs = torch.softmax(output, dim=1)
                top_prob, top_idx = torch.max(probs, 1)
                emonet_emotion = emotion_idx_to_label[top_idx.item()]
                emonet_confidence = top_prob.item()
            print(f"✅ EmoNet: {emonet_emotion} ({emonet_confidence:.2f})")
        except Exception as e:
            print(f"❌ EmoNet error: {e}")
            emonet_emotion = "neutral"
            emonet_confidence = 0.0

        # --- Cortex Fusion ---
        try:
            print("Running Cortex Fusion...")
            fused_response = cortex_fuse_response(
                question=question,
                logic=logicnet_output,
                memory=memorynet_output,
                creative=creativenet_output,
                emotion=emonet_emotion,
                pdf_chunks=PDF_CHUNKS
            )
            print("✅ Cortex Fusion completed")
        except Exception as e:
            print(f"❌ Cortex Fusion error: {e}")
            fused_response = "Response fusion failed"

        return jsonify({
            'route': route_label,
            'logicnet': logicnet_output,
            'memorynet': memorynet_output,
            'creativenet': creativenet_output,
            'emonet': {'emotion': emonet_emotion, 'confidence': emonet_confidence},
            'fused_response': fused_response
        })
        
    except Exception as e:
        print(f"❌ General error in /ask endpoint: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Server error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=8080)
