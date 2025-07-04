# models/memorynet/transformer_knowledge.py
import re
from typing import List, Tuple

# Transformer paper content chunks
TRANSFORMER_CHUNKS = [
    "The Transformer is a model architecture eschewing recurrence and instead relying entirely on an attention mechanism to draw global dependencies between input and output.",
    "Attention Is All You Need - The dominant sequence transduction models are based on complex recurrent or convolutional neural networks that include an encoder and a decoder.",
    "The Transformer allows for significantly more parallelization and can reach a new state of the art in translation quality after being trained for as little as twelve hours on eight P100 GPUs.",
    "Multi-Head Attention consists of several attention layers running in parallel. Instead of performing a single attention function with dmodel-dimensional keys, values and queries.",
    "Scaled Dot-Product Attention computes the attention function on a set of queries simultaneously, packed together into a matrix Q. The keys and values are also packed together into matrices K and V.",
    "The encoder is composed of a stack of N = 6 identical layers. Each layer has two sub-layers: multi-head self-attention mechanism and a simple position-wise fully connected feed-forward network.",
    "The decoder is also composed of a stack of N = 6 identical layers. In addition to the two sub-layers in each encoder layer, the decoder inserts a third sub-layer which performs multi-head attention over the output of the encoder stack.",
    "Self-attention, sometimes called intra-attention, is an attention mechanism relating different positions of a single sequence in order to compute a representation of the sequence.",
    "The Transformer achieves 28.4 BLEU on the WMT 2014 English-to-German translation task, improving over the existing best results by over 2 BLEU.",
    "Dot-product attention is identical to our algorithm, except for the scaling factor of 1/√dk. Additive attention computes the compatibility function using a feed-forward network with a single hidden layer.",
    "Residual connections are employed around each of the two sub-layers, followed by layer normalization. The output of each sub-layer is LayerNorm(x + Sublayer(x)).",
    "The Transformer follows an encoder-decoder architecture using stacked self-attention and point-wise, fully connected layers for both the encoder and decoder.",
    "Attention mechanisms have become an integral part of compelling sequence modeling and transduction models, allowing modeling of dependencies without regard to their distance in the input or output sequences.",
    "The number of operations required to relate signals from two arbitrary input or output positions grows in the distance between positions in convolutional models, but in the Transformer this is reduced to a constant number of operations.",
    "Positional encoding is added to the input embeddings to give the model some information about the relative or absolute position of the tokens in the sequence."
]

def chunk_text(text: str, chunk_size: int = 200) -> List[str]:
    """Split text into chunks of approximately chunk_size characters"""
    sentences = re.split(r'[.!?]+', text)
    chunks = []
    current_chunk = ""
    
    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue
            
        if len(current_chunk) + len(sentence) < chunk_size:
            current_chunk += sentence + ". "
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = sentence + ". "
    
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    return chunks

def calculate_relevance(query: str, chunk: str) -> float:
    """Calculate relevance score between query and chunk"""
    query_words = set(query.lower().split())
    chunk_words = set(chunk.lower().split())
    
    # Remove common stop words
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'can', 'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them'}
    query_words = query_words - stop_words
    chunk_words = chunk_words - stop_words
    
    if not query_words:
        return 0.0
    
    # Calculate word overlap
    overlap = len(query_words.intersection(chunk_words))
    return overlap / len(query_words)

def query_transformer_knowledge(query: str, top_k: int = 3) -> List[Tuple[str, float]]:
    """Query the Transformer knowledge base"""
    if not query.strip():
        return []
    
    # Calculate relevance scores for all chunks
    scored_chunks = []
    for chunk in TRANSFORMER_CHUNKS:
        score = calculate_relevance(query, chunk)
        if score > 0:  # Only include relevant chunks
            scored_chunks.append((chunk, score))
    
    # Sort by relevance score (descending) and return top_k
    scored_chunks.sort(key=lambda x: x[1], reverse=True)
    return scored_chunks[:top_k]

def get_transformer_concepts() -> List[str]:
    """Get key concepts from the Transformer paper"""
    return [
        "attention mechanism",
        "self-attention",
        "multi-head attention",
        "scaled dot-product attention",
        "encoder-decoder architecture",
        "positional encoding",
        "residual connections",
        "layer normalization",
        "transformer model",
        "sequence transduction",
        "neural networks",
        "machine translation",
        "BLEU score",
        "parallelization",
        "global dependencies"
    ]

if __name__ == "__main__":
    # Test the knowledge base
    test_queries = [
        "What is attention?",
        "How does the encoder work?",
        "What is multi-head attention?",
        "How does the transformer achieve parallelization?"
    ]
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        results = query_transformer_knowledge(query)
        for i, (chunk, score) in enumerate(results, 1):
            print(f"{i}. (Score: {score:.3f}) {chunk}") 