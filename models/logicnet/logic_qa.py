# models/logicnet/logic_qa.py

import requests

def answer_query(query, chunks, model="llama3"):
    """
    Enhanced logic-based answer generation using Ollama with local fallback
    """
    if not chunks:
        return "No context provided for analysis."
    
    context = "\n".join(chunks)
    prompt = (
        f"Context:\n{context}\n\n"
        f"Question: {query}\n"
        f"Answer using the context. Think step by step.\n"
        f"Final Answer:"
    )

    try:
        response = requests.post("http://localhost:11434/api/generate", json={
            "model": model,
            "prompt": prompt,
            "stream": False
        }, timeout=30)

        if response.status_code != 200:
            return local_logic_answer(query, chunks)
        
        result = response.json()
        
        # Check if response has the expected structure
        if "response" not in result:
            return local_logic_answer(query, chunks)
        
        response_text = result["response"]
        
        if "Final Answer:" in response_text:
            return response_text.split("Final Answer:")[-1].strip()
        else:
            return response_text.strip()

    except requests.exceptions.RequestException as e:
        # Fallback to local logic if Ollama is not available
        return local_logic_answer(query, chunks)
    except Exception as e:
        return local_logic_answer(query, chunks)

def local_logic_answer(query, chunks):
    """
    Local fallback logic when Ollama is not available
    """
    if not chunks:
        return "No context provided for analysis."
    
    # Convert everything to lowercase for matching
    query_lower = query.lower()
    
    # Simple keyword-based answer generation
    if "what is" in query_lower or "define" in query_lower:
        # Look for definitions in the context
        for chunk in chunks:
            if any(word in chunk.lower() for word in query_lower.split()):
                return f"Based on the document: {chunk[:200]}..."
    
    elif "how" in query_lower:
        # Look for process descriptions
        for chunk in chunks:
            if any(word in chunk.lower() for word in query_lower.split()):
                return f"According to the document: {chunk[:200]}..."
    
    elif "why" in query_lower:
        # Look for explanations
        for chunk in chunks:
            if any(word in chunk.lower() for word in query_lower.split()):
                return f"The document explains: {chunk[:200]}..."
    
    else:
        # General answer - find most relevant chunk
        best_chunk = ""
        best_score = 0
        
        for chunk in chunks:
            chunk_lower = chunk.lower()
            # Simple relevance scoring
            query_words = set(query_lower.split())
            chunk_words = set(chunk_lower.split())
            overlap = len(query_words.intersection(chunk_words))
            
            if overlap > best_score:
                best_score = overlap
                best_chunk = chunk
        
        if best_chunk:
            return f"Based on the document analysis: {best_chunk[:300]}..."
        else:
            return "The document doesn't contain specific information about this query."
    
    return "Unable to generate a logical response based on the provided context."
