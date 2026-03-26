# ============================================
# INGESTÃO DA BÍBLIA ARA PARA RAG
# ============================================

import json
import os
import numpy as np
from sentence_transformers import SentenceTransformer

# ============================================
# CONFIGURAÇÕES
# ============================================

INPUT_PATH = "data/biblia_ara.json"
OUTPUT_PATH = "data/biblia_ara_index.json"
MODEL_NAME = "all-MiniLM-L6-v2"


# ============================================
# FUNÇÕES AUXILIARES
# ============================================

def carregar_json(caminho):
    if not os.path.exists(caminho):
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho}")

    with open(caminho, "r", encoding="utf-8") as f:
        return json.load(f)


def validar_versiculo(v):
    campos_necessarios = ["livro", "capitulo", "versiculo", "texto"]

    for campo in campos_necessarios:
        if campo not in v:
            return False

    if not isinstance(v["texto"], str) or len(v["texto"].strip()) == 0:
        return False

    return True


def limpar_texto(texto):
    return texto.strip().replace("\n", " ")


# ============================================
# PIPELINE DE INGESTÃO
# ============================================

def main():
    print("📖 Iniciando ingestão da Bíblia ARA...")

    # 1. Carregar dados
    dados = carregar_json(INPUT_PATH)

    if not isinstance(dados, list):
        raise ValueError("O JSON deve ser uma LISTA de versículos")

    print(f"✔ {len(dados)} versículos carregados")

    # 2. Validar e limpar
    versiculos_validos = []

    for v in dados:
        if validar_versiculo(v):
            versiculos_validos.append({
                "livro": v["livro"],
                "capitulo": v["capitulo"],
                "versiculo": v["versiculo"],
                "texto": limpar_texto(v["texto"])
            })

    print(f"✔ {len(versiculos_validos)} versículos válidos")

    if len(versiculos_validos) == 0:
        raise ValueError("Nenhum versículo válido encontrado!")

    # 3. Preparar textos para embedding
    textos = [
        f"{v['livro']} {v['capitulo']}:{v['versiculo']} - {v['texto']}"
        for v in versiculos_validos
    ]

    print("🧠 Gerando embeddings...")

    # 4. Carregar modelo
    modelo = SentenceTransformer(MODEL_NAME)

    # 5. Gerar embeddings
    embeddings = modelo.encode(
        textos,
        show_progress_bar=True,
        convert_to_numpy=True
    )

    print(f"✔ Embeddings gerados: {embeddings.shape}")

    # 6. Salvar index
    print("💾 Salvando índice...")

    estrutura_saida = {
        "metadata": {
            "modelo": MODEL_NAME,
            "total_versiculos": len(versiculos_validos)
        },
        "versiculos": versiculos_validos,
        "embeddings": embeddings.tolist()
    }

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(estrutura_saida, f, ensure_ascii=False)

    print(f"✅ Índice salvo em: {OUTPUT_PATH}")


# ============================================
# EXECUÇÃO
# ============================================

if __name__ == "__main__":
    main()