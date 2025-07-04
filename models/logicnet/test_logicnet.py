# models/logicnet/test_logicnet.py

from logic_qa import answer_query

# Sample test chunks (normally from MemoryNet)
chunks = [
    "FAISS is a library developed by Facebook for efficient similarity search and clustering of dense vectors.",
    "It enables fast retrieval in vector databases, especially useful for LLM RAG pipelines.",
    "FAISS supports CPU and GPU execution and is widely used in semantic search."
]

print("🧠 Ask a question:")
query = input("> ")

answer = answer_query(query, chunks)
print("\n🧠 Final Answer:\n", answer)
