import json
import numpy as np
from sentence_transformers import SentenceTransformer

modelo = SentenceTransformer("all-MiniLM-L6-v2")

with open("data/biblia_ara_index.json", "r", encoding="utf-8") as f:
    data = json.load(f)

versiculos = data["versiculos"]
embeddings = np.array(data["embeddings"])


def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def buscar_versiculos(pergunta, top_k=5):
    query = modelo.encode(pergunta)

    scores = np.array([
        cosine_similarity(query, emb) for emb in embeddings
    ])

    idx = np.argsort(scores)[-top_k:][::-1]

    return [versiculos[i] for i in idx]