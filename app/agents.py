import requests
import json
from rag import buscar_versiculos
from storage import save_output, buscar_memoria

# =========================
# CORE LLM
# =========================
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3:8b-instruct-q4_K_M"

# Sugestão:
# | Agente     | Temperatura |
# | ---------- | ----------- |
# | Curador    | 0.1         |
# | Exegeta    | 0.2         |
# | Integrador | 0.4         |
# | Refinador  | 0.3         |
# | Crítico    | 0.0         |
def chamar_llm(prompt, temperature=0.2):
    for _ in range(3):
        try:
            response = requests.post(
                OLLAMA_URL,
                json={
                    "model": MODEL,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": temperature,
                    }
                }
            )
            return response.json()["response"]
        except:
            continue

    return "Erro ao chamar modelo"

def chamar_llm_json(prompt, temperature=0.0):
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

# =========================
# AGENTE CURADOR
# =========================
def agente_curador(contexto, run_id, iteracao):
    resultados = buscar_versiculos(contexto["pergunta"])
    memorias = buscar_memoria(contexto["pergunta"], tipo="curador")

    prompt = f"""
    PERGUNTA:
    {contexto['pergunta']}

    MEMÓRIAS DE SELEÇÃO ANTERIOR:
    {memorias}

    TEXTOS RECUPERADOS:
    {resultados}

    TAREFA:
    Selecione até 5 textos bíblicos mais relevantes considerando:
    - Similaridade com a pergunta
    - Profundidade existencial
    - Conexão com memórias anteriores

    IMPORTANTE:
    - Priorize a similaridade com a pergunta
    - Use as memórias como referência de qualidade, mas NÃO copie diretamente

    Para cada texto:
    - Referência
    - Resumo
    - Relevância
    """

    resposta = chamar_llm(prompt, temperature=0.1)

    save_output(run_id, iteracao, "curador",
                contexto["pergunta"], str(resultados), resposta)

    return resposta

# =========================
# AGENTE EXEGETA
# =========================
def agente_exegeta(textos, contexto, run_id, iteracao):
    prompt = f"""
    TEXTOS:
    {textos}

    TAREFA:
    Faça análise exegética profunda:

    - Contexto histórico
    - Significado original
    - Conflito humano envolvido

    Evite generalizações.
    """

    resposta = chamar_llm(prompt, temperature=0.2)

    save_output(run_id, iteracao, "exegeta",
                contexto["pergunta"], textos, resposta)

    return resposta

# =========================
# AGENTE INTEGRADOR
# =========================
def agente_integrador(analise, contexto, run_id, iteracao):
    memorias = buscar_memoria(contexto["pergunta"], tipo="integrador")
    
    prompt = f"""
    BASE:
    {analise}

    PERGUNTA:
    {contexto['pergunta']}


    MEMÓRIAS DE RESPOSTAS PROFUNDAS:
    {memorias}

    TAREFA:
    Gere uma resposta existencial e pastoral:
    - Clara
    - Profunda
    - Conectada à experiência humana

    NÃO copie as memórias diretamente, use as como referência de qualidade

    Busque originalidade com consistência
    """

    resposta = chamar_llm(prompt, temperature=0.4)

    save_output(run_id, iteracao, "integrador",
                contexto["pergunta"], analise, resposta)

    return resposta

def validar_critico(resultado):
    campos = ["fidelidade", "clareza", "profundidade", "score_total", "feedback", "decisao"]

    for c in campos:
        if c not in resultado:
            return False

    return True

# =========================
# AGENTE CRÍTICO (JSON)
# =========================
def agente_critico(resposta, contexto, run_id, iteracao):
    prompt = f"""
    RESPOSTA:
    {resposta}

    Avalie:

    1. Fidelidade bíblica (0-10)
    2. Clareza (0-10)
    3. Profundidade (0-10)

    IMPORTANTE:
    - Retorne APENAS JSON válido
    - NÃO escreva nenhum texto antes ou depois

    FORMATO EXATO:
    {{
      "fidelidade": int,
      "clareza": int,
      "profundidade": int,
      "score_total": int,
      "feedback": "texto",
      "decisao": "APROVAR" ou "REVISAR"
    }}
    """

    resultado = chamar_llm_json(prompt)

    if not validar_critico(resultado):
        resultado = {
            "erro": True,
            "score_total": 0,
            "feedback": "JSON inválido",
            "decisao": "REVISAR"
        }

    save_output(run_id, iteracao, "critico",
                contexto["pergunta"], resposta,
                json.dumps(resultado, ensure_ascii=False),
                resultado.get("score_total"),
                resultado.get("feedback"))

    return resultado

# =========================
# AGENTE REFINADOR
# =========================
def agente_refinador(resposta, feedback, contexto, run_id, iteracao):
    prompt = f"""
    RESPOSTA ORIGINAL:
    {resposta}

    FEEDBACK:
    {feedback}

    PERGUNTA:
    {contexto['pergunta']}

    TAREFA:
    Reescreva a resposta corrigindo os problemas.

    - Mais fidelidade bíblica
    - Mais profundidade
    - Mais clareza
    - Mais conexão humana
    """

    resposta_refinada = chamar_llm(prompt, temperature=0.3)

    save_output(run_id, iteracao, "refinador",
                contexto["pergunta"], resposta, resposta_refinada)

    return resposta_refinada