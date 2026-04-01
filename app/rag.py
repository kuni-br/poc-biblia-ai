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

# | Perfil        | alpha | beta |
# | ------------- | ----- | ---- |
# | Mais técnico  | 0.8   | 0.2  |
# | Equilibrado   | 0.7   | 0.3  |
# | Mais profundo | 0.5   | 0.5  |
def buscar_versiculos(pergunta, top_k=5, alpha=0.7, beta=0.3):
    query = modelo.encode(pergunta)

    scores = []

    for i, emb in enumerate(embeddings):
        sim = cosine_similarity(query, emb)

        # fallback se não tiver densidade
        densidade = versiculos[i].get("densidade", 5.0)

        score_final = sim * alpha + densidade * beta

        scores.append(score_final)

    idx = np.argsort(scores)[-top_k:][::-1]

    return [versiculos[i] for i in idx]