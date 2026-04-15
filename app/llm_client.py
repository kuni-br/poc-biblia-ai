import json
import os
import requests
from openai import OpenAI
from dotenv import load_dotenv

# Carrega o .env explicitamente
load_dotenv()

# =========================
# CONFIGURAÇÃO
# =========================
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "deepseek")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_MODEL = "deepseek-chat"

# Debug: mostra o que foi carregado
# print(f"🔧 LLM_PROVIDER = '{LLM_PROVIDER}'")
# print(f"🔑 DEEPSEEK_API_KEY = {'✅ Configurada' if DEEPSEEK_API_KEY else '❌ NÃO CONFIGURADA'}")
# print(f"📦 DEEPSEEK_MODEL = {DEEPSEEK_MODEL}")

# Configuração Ollama (mantida para fallback)
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3:8b-instruct-q4_K_M"

# =========================
# CLIENTE DEEPSEEK
# =========================
deepseek_client = None
if DEEPSEEK_API_KEY and DEEPSEEK_API_KEY != "sua-chave-aqui":
    deepseek_client = OpenAI(
        api_key=DEEPSEEK_API_KEY,
        base_url="https://api.deepseek.com"
    )

# =========================
# FUNÇÃO UNIFICADA DE CHAMADA
# =========================
def chamar_llm(prompt, temperature=0.2):
    """Chama o LLM configurado (DeepSeek ou Ollama)"""
    
    if LLM_PROVIDER == "deepseek" and deepseek_client:
        return _chamar_deepseek(prompt, temperature)
    else:
        return _chamar_ollama(prompt, temperature)


def _chamar_deepseek(prompt, temperature):
    """Chama a API do DeepSeek usando o cliente OpenAI"""
    for _ in range(3):
        try:
            response = deepseek_client.chat.completions.create(
                model=DEEPSEEK_MODEL,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature,
                max_tokens=4096  # valor seguro para respostas longas
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Erro na chamada DeepSeek (tentativa {_+1}): {e}")
            continue
    
    return "Erro ao chamar modelo DeepSeek"


def _chamar_ollama(prompt, temperature):
    """Chama o Ollama local (código original preservado)"""
    for _ in range(3):
        try:
            response = requests.post(
                OLLAMA_URL,
                json={
                    "model": OLLAMA_MODEL,
                    "prompt": prompt,
                    "stream": False,
                    "options": {"temperature": temperature}
                },
                timeout=60
            )
            return response.json()["response"]
        except Exception as e:
            print(f"Erro na chamada Ollama (tentativa {_+1}): {e}")
            continue
    
    return "Erro ao chamar modelo Ollama"


def chamar_llm_json(prompt, temperature=0.0):
    """Chama o LLM e retorna JSON estruturado"""
    raw = chamar_llm(prompt, temperature=temperature)

    try:
        return json.loads(raw)
    except:
        # tenta extrair JSON dentro do texto
        try:
            start = raw.find("{")
            end = raw.rfind("}") + 1
            json_str = raw[start:end]
            return json.loads(json_str)
        except:
            return {
                "erro": True,
                "raw": raw,
                "score_total": 0,
                "feedback": "Erro ao interpretar JSON",
                "decisao": "REVISAR"
            }