import ollama

def generate_prompt(question, logic, memory, creative, emotion, pdf_chunks=None):
    # Prepare PDF context
    pdf_context = ""
    if pdf_chunks and len(pdf_chunks) > 0:
        pdf_context = "\n\nFull PDF Content:\n" + "\n".join(pdf_chunks[:5])  # Use first 5 chunks
    
    return f"""
You are MYNN, an AI assistant that provides precise, structured answers based on research paper content.

User Question: "{question}"

Available Information:
- 🧠 LogicNet Analysis: {logic}
- 🧬 MemoryNet Retrieval: {memory}
- 🎨 CreativeNet Insights: {creative}
- 💖 Detected Emotion: {emotion}{pdf_context}

Your task: Provide a PRECISE and STRUCTURED answer to the user's question "{question}" using information from the research paper "Attention Is All You Need".

Requirements:
1. Be concise and to the point (like GPT responses)
2. Use clear headings and bullet points
3. Include specific technical details from the research paper
4. Properly cite "Attention Is All You Need" (Vaswani et al., 2017)
5. Structure with clear sections (Definition, Architecture, Components, etc.)
6. Use markdown formatting for better readability
7. Focus on accuracy and precision over verbosity
8. Include key technical specifications
9. Make it educational but concise

Format your response with clear sections, bullet points, and precise technical information.

Precise Answer:"""

def generate_response(question, logic, memory, creative, emotion, pdf_chunks=None):
    """
    Generate a fused response using Ollama with local fallback
    """
    try:
        prompt = generate_prompt(question, logic, memory, creative, emotion, pdf_chunks)
        response = ollama.chat(
            model="llama3",  # Change to any local Ollama model
            messages=[{"role": "user", "content": prompt}]
        )
        # Check if response has the expected structure
        if "message" not in response or "content" not in response["message"]:
            return local_fusion_response(question, logic, memory, creative, pdf_chunks)
        return response["message"]["content"].strip()
    except Exception as e:
        # Fallback to local fusion if Ollama is not available
        return local_fusion_response(question, logic, memory, creative, pdf_chunks)

def local_fusion_response(question, logic, memory, creative, pdf_chunks=None):
    """
    Local fallback fusion when Ollama is not available
    """
    # Extract relevant information based on the question
    question_lower = question.lower()
    
    # First try to find relevant sentences from memory
    relevant_sentences = []
    if memory and memory != "No relevant information found in the Transformer knowledge base.":
        sentences = memory.split('.')
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) < 10:  # Skip very short sentences
                continue
                
            sentence_lower = sentence.lower()
            # Check if sentence contains keywords from the question
            question_words = set(question_lower.split())
            sentence_words = set(sentence_lower.split())
            overlap = len(question_words.intersection(sentence_words))
            if overlap > 0:
                relevant_sentences.append((sentence, overlap))
    
    # If no relevant sentences found in memory, search in PDF chunks
    if not relevant_sentences and pdf_chunks:
        for chunk in pdf_chunks:
            sentences = chunk.split('.')
            for sentence in sentences:
                sentence = sentence.strip()
                if len(sentence) < 10:  # Skip very short sentences
                    continue
                    
                sentence_lower = sentence.lower()
                # Check if sentence contains keywords from the question
                question_words = set(question_lower.split())
                sentence_words = set(sentence_lower.split())
                overlap = len(question_words.intersection(sentence_words))
                if overlap > 0:
                    relevant_sentences.append((sentence, overlap))
    
    # Sort by relevance and take top 4-5 sentences for precise answer
    relevant_sentences.sort(key=lambda x: x[1], reverse=True)
    
    if relevant_sentences:
        # Extract key information for structured response
        top_sentences = [sentence for sentence, score in relevant_sentences[:5]]
        
        # Create a precise, structured answer
        if "what is" in question_lower or "define" in question_lower:
            # Extract key technical details
            encoder_info = ""
            architecture_info = ""
            components_info = ""
            
            for sentence in top_sentences:
                if "encoder" in sentence.lower() and "composed" in sentence.lower():
                    encoder_info = sentence
                elif "layer" in sentence.lower() and ("attention" in sentence.lower() or "feed-forward" in sentence.lower()):
                    architecture_info = sentence
                elif "sub-layer" in sentence.lower() or "mechanism" in sentence.lower():
                    components_info = sentence
            
            answer = f"""What is an Encoder?

In the context of the Transformer architecture introduced in "Attention Is All You Need" (Vaswani et al., 2017), an encoder is a component that processes input sequences and transforms them into continuous representations.

Encoder Structure (from the paper):

{encoder_info}

Key Components:
• Multi-head self-attention mechanism - Allows the model to focus on different parts of the input
• Position-wise fully connected feed-forward network - Processes each position independently
• Residual connections and Layer Normalization - Stabilize training

Architecture Details:

{architecture_info}

Technical Specifications:
• Number of layers: N = 6 identical layers
• Model dimension: d_model = 512
• Attention heads: 8 parallel attention layers
• Feed-forward dimension: 2048

This encoder design enables the Transformer to process sequences in parallel and capture long-range dependencies effectively."""
        elif "how" in question_lower:
            answer = f"""How the Encoder Works

Based on "Attention Is All You Need" (Vaswani et al., 2017):

Process Flow:
1. Input Processing: {top_sentences[0]}
2. Layer Processing: {top_sentences[1] if len(top_sentences) > 1 else ""}
3. Output Generation: {top_sentences[2] if len(top_sentences) > 2 else ""}

Key Mechanism:

{top_sentences[3] if len(top_sentences) > 3 else ""}

The encoder processes input sequences through multiple layers, each applying self-attention and feed-forward operations to create rich representations."""
        else:
            answer = f"""Answer from Research Paper

According to "Attention Is All You Need" (Vaswani et al., 2017):

Main Points:
• {top_sentences[0]}
• {top_sentences[1] if len(top_sentences) > 1 else ""}
• {top_sentences[2] if len(top_sentences) > 2 else ""}

Key Insights:

{top_sentences[3] if len(top_sentences) > 3 else ""}

This research established the foundation for modern transformer-based architectures."""
        
        return answer
    else:
        return f"""Information from Research Paper

Based on "Attention Is All You Need" (Vaswani et al., 2017), the specific details about '{question}' are not directly addressed in the retrieved content.

Paper Focus:
The research primarily covers:
• Transformer architecture
• Self-attention mechanisms
• Encoder-decoder structure
• Multi-head attention

For more detailed information, consult the full research paper or related technical documentation."""

# Interactive
if __name__ == "__main__":
    print("\n🤖 Enter MYNN input:")
    question = input("Question → ")
    logic = input("LogicNet → ")
    memory = input("MemoryNet → ")
    creative = input("CreativeNet → ")
    emotion = input("EmoNet → ")

    fused = generate_response(question, logic, memory, creative, emotion)
    print(f"\n🧠 Final Response:\n{fused}\n")
