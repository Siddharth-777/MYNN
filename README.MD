# MYNN: Mycelium-Inspired Neural Network

## Overview
MYNN is an AI system inspired by the decentralized communication of mycelium networks in nature. It integrates four neural modules—LogicNet, MemoryNet, CreativeNet, and Emonet—to process queries with reasoning, context, creativity, and emotional insight. Built with custom RAG, classifiers, and creativity models, MYNN delivers metaphor-rich, impactful responses.

## Features
- **Modular Design**: Four modules (LogicNet, MemoryNet, CreativeNet, Emonet) handle distinct aspects of query processing.
- **Mycelium Controller**: Routes queries to appropriate modules for efficient processing.
- **LogicNet**: Uses chain-of-thought reasoning for precise, logical answers.
- **MemoryNet**: Employs RAG for contextual information retrieval.
- **CreativeNet**: Generates novel, metaphorical associations.
- **Emonet**: Detects sentiment and intent using DistilBERT trained on GoEmotions.
- **Full-Stack Support**: Includes Flask-based API with planned web UI integration.

## Folder Structure
- `models/`: Core modules.
  - `mycelium_controller/`: Query routing logic.
  - `logicnet/`: Reasoning module.
  - `memorynet/`: RAG-based memory system.
  - `creativenet/`: Metaphor generation.
  - `emonet/`: Emotion classification.
- `data/`: Datasets (`goemotions_real_clean.csv`, `emotions.json`).
- `preprocess/`: Data preprocessing scripts.
- `test/`: Inference scripts (e.g., `test_logicnet.py`, `test_emonet.py`).
- `cortex_fusion/`: Response fusion logic.
- `mynn_cli.py`: Main runner script.

## Installation
1. **Clone Repository**:
   ```bash
   git clone https://github.com/your-repo/mynn.git
   cd mynn
   ```
2. **Set Up Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/Scripts/activate  # Windows
   source venv/bin/activate     # Linux/Mac
   ```
3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   Requires `torch`, `pandas`, `scikit-learn`, `sentence_transformers`, `faiss-cpu`, `flask`.
4. **Prepare Data**:
   - Place `goemotions_real_clean.csv` and `emotions.json` in `data/`.
   - Ensure `cortex_data.csv` is available.
5. **Train Models**:
   ```bash
   python models/emonet/train.py
   python models/cortex_fusion/train.py
   ```
6. **Run CLI**:
   ```bash
   python mynn_cli.py
   ```

## Usage
- **Run CLI**:
   ```bash
   python mynn_cli.py
   ```
   Input a query (e.g., "How is a forest like a neural network?") to receive a fused response.
- **Example**:
   - Query: "How is a forest like a neural network?"
   - Output: "A forest resembles a neural network through interconnected layers, with roots and branches sharing signals to form knowledge."
- **Web UI**: Flask-based interface in development for browser interaction.

## Technical Details
- **LogicNet**: Transformer-based reasoning with ShareGPT datasets.
- **MemoryNet**: FAISS-powered vector search for document embeddings.
- **CreativeNet**: Vector blending for creative analogies.
- **Emonet**: DistilBERT-based emotion classification.
- **CortexFusion**: Fuses module outputs for cohesive responses.
- **Hardware**: Supports CPU/GPU; recommended 16GB RAM, 8GB+ VRAM GPU.

## Error Handling
- **FileNotFoundError**: Verify model files (`emonet_model.pt`, `vectorizer.pkl`) exist.
- **ImportError**: Ensure `models/` is in `sys.path`.
- **RuntimeError**: Check input dimensions in `controller_model.py`.
- **CSV Issues**: Confirm `data.csv` has `text` and `label` columns.

## Future Enhancements
- Web UI with React/Streamlit.
- Local LLM integration via Ollama.
- Dynamic path handling with `pathlib`.
- Scalability for larger datasets.

## Contributing
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/YourFeature`).
3. Commit changes (`git commit -m 'Add YourFeature'`).
4. Push to branch (`git push origin feature/YourFeature`).
5. Open a pull request.

## License
MIT License.

## Acknowledgments
- Inspired by mycelium networks.
- Built with PyTorch, FAISS, SentenceTransformers, Flask.
- Uses HuggingFace datasets (e.g., GoEmotions).

## YT  VIDEO
https://youtu.be/X02f8di1KxI
