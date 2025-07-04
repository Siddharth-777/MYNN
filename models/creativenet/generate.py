# generate.py
from .utils import embed_text, get_embedding_model, cosine_similarity
from .perturber import perturb_vector
from .decoder import decode_vector

def generate_creative_associations(prompt, top_k=3):
    model = get_embedding_model()
    base_vec = embed_text(prompt, model)

    outputs = []
    for _ in range(30):
        new_vec = perturb_vector(base_vec)
        sim = cosine_similarity(base_vec, new_vec)
        if 0.3 < sim < 0.8:
            phrase = decode_vector(new_vec)[0]
            outputs.append((phrase, sim))

    # Remove duplicates and return top-k by novelty
    seen = set()
    unique_outputs = []
    for phrase, score in outputs:
        if phrase not in seen:
            seen.add(phrase)
            unique_outputs.append((phrase, score))
        if len(unique_outputs) >= top_k:
            break

    return [f"{phrase} → Similarity: {round(score, 3)}" for phrase, score in unique_outputs]
