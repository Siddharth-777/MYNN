# utils.py
from sentence_transformers import SentenceTransformer
import numpy as np

_model = None

def get_embedding_model():
    global _model
    if _model is None:
        _model = SentenceTransformer("hkunlp/instructor-xl")
    return _model

def embed_text(text, model):
    return np.array(model.encode(text, normalize_embeddings=True))

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
