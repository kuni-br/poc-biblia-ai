import sqlite3
from datetime import datetime
import uuid

DB_PATH = "data/logs.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS runs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        run_id TEXT,
        pergunta TEXT,
        agente TEXT,
        resposta TEXT,
        timestamp TEXT
    )
    """)

    conn.commit()
    conn.close()


def save_output(pergunta, agente, resposta):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    run_id = datetime.now().isoformat()

    c.execute("""
    INSERT INTO runs (run_id, pergunta, agente, resposta, timestamp)
    VALUES (?, ?, ?, ?, ?)
    """, (run_id, pergunta, agente, resposta, datetime.now().isoformat()))

    conn.commit()
    conn.close()