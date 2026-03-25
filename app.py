import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3:8b-instruct-q4_K_M"

def chamar_llm(prompt):
    try:
        response = requests.post(OLLAMA_URL, json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.2  # menos alucinação
            }
        })

        response.raise_for_status()
        return response.json()["response"]

    except Exception as e:
        return f"[ERRO LLM]: {str(e)}"