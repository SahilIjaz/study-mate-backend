import faiss
import numpy as np

DIMENSION = 384  # must match embeddings.py

index = faiss.IndexFlatL2(DIMENSION)
chunk_store: dict = {}


def add_chunks(chunks: list):
    for chunk in chunks:
        embedding = np.array(chunk["embedding"], dtype="float32").reshape(1, -1)
        faiss_id = index.ntotal
        index.add(embedding)
        chunk_store[faiss_id] = {
            "text": chunk["text"],
            "source_file": chunk["source_file"]
        }


def query_chunks(query_embedding: list, top_k: int = 5) -> list:
    if index.ntotal == 0:
        return []
    query_vec = np.array(query_embedding, dtype="float32").reshape(1, -1)
    distances, indices = index.search(query_vec, min(top_k, index.ntotal))
    results = []
    for i in indices[0]:
        if i != -1 and i in chunk_store:
            results.append(chunk_store[i])
    return results