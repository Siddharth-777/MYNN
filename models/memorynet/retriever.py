from sentence_transformers import SentenceTransformer
import faiss
import json
import numpy as np
import os

MODEL_NAME = "hkunlp/instructor-xl"
BASE_DIR = os.path.dirname(__file__)
INDEX_FILE = os.path.join(BASE_DIR, "memorynet.index")
METADATA_FILE = os.path.join(BASE_DIR, "metadata.json")


def load_model():
    return SentenceTransformer(MODEL_NAME)

def load_index():
    return faiss.read_index(INDEX_FILE)

def load_chunks():
    with open(METADATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def query_index(query, top_k=3):
    model = load_model()
    index = load_index()
    chunks = load_chunks()

    embedding = model.encode(
        [["Represent the scientific text: ", query]],
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    D, I = index.search(embedding, top_k)
    results = [(chunks[i], float(D[0][idx])) for idx, i in enumerate(I[0])]
    return results

if __name__ == "__main__":
    query = input("🔍 Ask MYNN something: ")
    results = query_index(query)
    for i, (chunk, score) in enumerate(results, 1):
        print(f"\n#{i} (score: {score:.4f})\n{chunk}")
