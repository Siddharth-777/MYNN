# decoder.py
from .utils import embed_text, get_embedding_model, cosine_similarity
import numpy as np
import os

# Get the directory where this file is located
current_dir = os.path.dirname(os.path.abspath(__file__))
concepts_file = os.path.join(current_dir, "transformer_concepts.txt")

with open(concepts_file, "r") as f:
    concepts = [line.strip() for line in f.readlines() if line.strip()]

model = get_embedding_model()
concept_vectors = [embed_text(c, model) for c in concepts]

def decode_vector(vec, top_k=1):
    sims = [cosine_similarity(vec, cvec) for cvec in concept_vectors]
    sorted_indices = np.argsort(sims)[::-1][:top_k]
    return [concepts[i] for i in sorted_indices]
