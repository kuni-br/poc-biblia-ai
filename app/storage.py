import sqlite3
import json

DB_PATH = "data/logs.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

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