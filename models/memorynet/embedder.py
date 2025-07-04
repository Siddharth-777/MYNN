from sentence_transformers import SentenceTransformer
import json
import faiss
import numpy as np
import os

MODEL_NAME = "hkunlp/instructor-xl"  # or use "sentence-transformers/all-MiniLM-L6-v2"
DATA_FILE = "sample_chunks.json"
INDEX_FILE = "memorynet.index"
METADATA_FILE = "metadata.json"

def load_chunks(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def embed_chunks(chunks):
    print("Loading model...")
    model = SentenceTransformer(MODEL_NAME)
    print("Embedding chunks...")
    embeddings = model.encode(
        [["Represent the scientific text: ", chunk] for chunk in chunks],
        convert_to_numpy=True,
        normalize_embeddings=True
    )
    return embeddings

def build_faiss_index(embeddings):
    dim = embeddings.shape[1]
    index = faiss.IndexFlatIP(dim)  # inner product for normalized embeddings
    index.add(embeddings)
    return index

def save_index(index, path):
    faiss.write_index(index, path)

def save_metadata(chunks, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=2)

if __name__ == "__main__":
    chunks = load_chunks(DATA_FILE)
    embeddings = embed_chunks(chunks)
    index = build_faiss_index(embeddings)
    save_index(index, INDEX_FILE)
    save_metadata(chunks, METADATA_FILE)
    print("✅ MemoryNet index built and saved.")
