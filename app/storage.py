import sqlite3
import json

DB_PATH = "data/logs.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # =========================
    # LOG DE EXECUÇÕES (mantido)
    # =========================
    c.execute("""
    CREATE TABLE IF NOT EXISTS runs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        run_id TEXT,
        iteracao INTEGER,
        agente TEXT,
        pergunta TEXT,
        entrada TEXT,
        saida TEXT,
        score INTEGER,
        feedback TEXT,
        raw_json TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # =========================
    # MEMÓRIA SEMÂNTICA
    # =========================
    c.execute("""
    CREATE TABLE IF NOT EXISTS memoria (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tipo TEXT,  -- "curador" ou "integrador"
        pergunta TEXT,
        conteudo TEXT,
        embedding BLOB,
        score REAL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        vezes_usado INTEGER DEFAULT 0,
        ultimo_uso DATETIME,
        peso REAL DEFAULT 1.0
    )
    """)

    # =========================
    # VERSÍCULOS COM METADADOS
    # =========================
    c.execute("""
    CREATE TABLE IF NOT EXISTS versiculos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        referencia TEXT,
        texto TEXT,
        embedding BLOB,
        densidade REAL DEFAULT 5.0,
        vezes_usado INTEGER DEFAULT 0,
        score_medio REAL DEFAULT 0
    )
    """)

    conn.commit()
    conn.close()

def save_output(run_id, iteracao, agente, pergunta, entrada, saida, score=None, feedback=None):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    raw_json = None

    # se saída for JSON string válido
    if isinstance(saida, str):
        try:
            parsed = json.loads(saida)
            raw_json = json.dumps(parsed, ensure_ascii=False)
        except:
            raw_json = saida  # salva mesmo inválido

    c.execute("""
    INSERT INTO runs (
        run_id, iteracao, agente, pergunta, entrada, saida,
        score, feedback, raw_json
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        run_id,
        iteracao,
        agente,
        pergunta,
        str(entrada),
        str(saida),
        score,
        feedback,
        raw_json
    ))

    conn.commit()
    conn.close()

import numpy as np
from sentence_transformers import SentenceTransformer

modelo = SentenceTransformer("all-MiniLM-L6-v2")

# =========================
# MEMÓRIA SEMÂNTICA
# =========================
def salvar_memoria(tipo, pergunta, conteudo, score):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    embedding = modelo.encode(pergunta).astype("float32").tobytes()

    c.execute("""
    INSERT INTO memoria (tipo, pergunta, conteudo, embedding, score)
    VALUES (?, ?, ?, ?, ?)
    """, (
        tipo,
        pergunta,
        conteudo,
        embedding,
        score
    ))

    conn.commit()
    conn.close()

import datetime

def buscar_memoria(pergunta, tipo, top_k=3):
    import datetime

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    query_emb = modelo.encode(pergunta)

    c.execute("""
    SELECT id, pergunta, conteudo, embedding, score, peso, vezes_usada, ultimo_uso
    FROM memoria
    WHERE tipo = ?
    """, (tipo,))

    rows = c.fetchall()

    resultados = []
    agora = datetime.datetime.now()

    # ranking híbrido memória
    # | Estratégia        | Sim | Score |
    # | ----------------- | --- | ----- |
    # | conservador       | 0.8 | 0.2   |
    # | equilibrado       | 0.7 | 0.3   |
    # | aprendizado forte | 0.6 | 0.4   |
    for row in rows:
        id_, p, conteudo, emb_blob, score, peso, vezes_usada, ultimo_uso = row

        emb = np.frombuffer(emb_blob, dtype=np.float32)

        # =========================
        # 1. Similaridade semântica
        # =========================
        sim = np.dot(query_emb, emb) / (
            np.linalg.norm(query_emb) * np.linalg.norm(emb)
        )

        # =========================
        # 2. Fator de recência
        # =========================
        if ultimo_uso:
            try:
                ultimo_uso_dt = datetime.datetime.fromisoformat(ultimo_uso)
                dias_sem_uso = (agora - ultimo_uso_dt).days
                fator_recencia = max(0.5, 1 - (dias_sem_uso * 0.05))
            except:
                fator_recencia = 1.0
        else:
            fator_recencia = 1.0

        # =========================
        # 3. Fator de frequência
        # =========================
        fator_frequencia = 1 + (vezes_usada * 0.05)

        # =========================
        # 4. Score final híbrido
        # =========================
        score_final = (
            sim * 0.5 +
            score * 0.06 +
            peso * 0.2 +
            fator_recencia * 0.05 +
            fator_frequencia * 0.05
        )

        resultados.append((score_final, id_, conteudo))

    # =========================
    # Ordenar melhores memórias
    # =========================
    resultados.sort(reverse=True)

    top_resultados = resultados[:top_k]

    # =========================
    # Atualizar uso das memórias selecionadas
    # =========================
    for _, id_, _ in top_resultados:
        c.execute("""
        UPDATE memoria
        SET vezes_usada = COALESCE(vezes_usada, 0) + 1,
            ultimo_uso = ?
        WHERE id = ?
        """, (agora.isoformat(), id_))

    conn.commit()
    conn.close()

    # =========================
    # Retorno apenas do conteúdo
    # =========================
    return [r[2] for r in top_resultados]

# Valor	Comportamento
# 0.6	reforça mais memórias
# 0.7	equilibrado
# 0.8	reforço mais preciso

# Valor	Efeito
# 0.05	aprendizado lento
# 0.1	equilibrado
# 0.2	aprendizado rápido

def reforcar_memorias(pergunta, tipo, incremento=0.1, threshold_sim=0.7):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    query_emb = modelo.encode(pergunta)

    c.execute("""
    SELECT id, embedding, peso
    FROM memoria
    WHERE tipo = ?
    """, (tipo,))

    rows = c.fetchall()

    for id_, emb_blob, peso in rows:
        emb = np.frombuffer(emb_blob, dtype=np.float32)

        # =========================
        # Similaridade
        # =========================
        den = (np.linalg.norm(query_emb) * np.linalg.norm(emb))
        if den == 0:
            continue

        sim = np.dot(query_emb, emb) / den

        # =========================
        # Reforço somente se relevante
        # =========================
        if sim >= threshold_sim:
            novo_peso = (peso or 1.0) + incremento

            # limitar crescimento
            novo_peso = min(novo_peso, 3.0)

            c.execute("""
            UPDATE memoria
            SET peso = ?
            WHERE id = ?
            """, (novo_peso, id_))

    conn.commit()
    conn.close()

import datetime

def aplicar_decay(fator_global=0.01, fator_tempo=0.02):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    agora = datetime.datetime.now()

    c.execute("""
    SELECT id, peso, ultimo_uso
    FROM memoria
    """)

    rows = c.fetchall()

    for id_, peso, ultimo_uso in rows:

        peso_atual = peso if peso is not None else 1.0

        # =========================
        # 1. Decay global (leve)
        # =========================
        peso_novo = peso_atual * (1 - fator_global)

        # =========================
        # 2. Decay por tempo
        # =========================
        if ultimo_uso:
            try:
                ultimo_uso_dt = datetime.datetime.fromisoformat(ultimo_uso)
                dias_sem_uso = (agora - ultimo_uso_dt).days

                # quanto mais dias → mais decay
                decay_tempo = 1 - (dias_sem_uso * fator_tempo)

                # limite inferior
                decay_tempo = max(0.5, decay_tempo)

                peso_novo *= decay_tempo

            except:
                pass

        # =========================
        # 3. Limite inferior
        # =========================
        peso_novo = max(0.1, peso_novo)

        c.execute("""
        UPDATE memoria
        SET peso = ?
        WHERE id = ?
        """, (peso_novo, id_))

    conn.commit()
    conn.close()

def limpar_memorias(peso_min=0.2):
    import sqlite3

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
    DELETE FROM memoria
    WHERE peso < ?
    """, (peso_min,))

    deletadas = c.rowcount

    conn.commit()
    conn.close()

    return deletadas