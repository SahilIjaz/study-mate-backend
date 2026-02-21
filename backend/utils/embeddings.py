import hashlib
import numpy as np

DIMENSION = 384

def _text_to_vector(text: str) -> list:
    vector = np.zeros(DIMENSION, dtype="float32")
    words = text.lower().split()
    for word in words:
        hash_val = int(hashlib.md5(word.encode()).hexdigest(), 16)
        index = hash_val % DIMENSION
        vector[index] += 1.0
    norm = np.linalg.norm(vector)
    if norm > 0:
        vector = vector / norm
    return vector.tolist()

def get_embeddings(texts: list) -> list:
    return [_text_to_vector(t) for t in texts]

def get_single_embedding(text: str) -> list:
    return _text_to_vector(text)