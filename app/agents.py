import requests
import json
from .rag import buscar_versiculos
from .storage import save_output, buscar_memoria
from .llm_client import chamar_llm, chamar_llm_json

# ============================
# | Sugestão:                |
# | Agente     | Temperatura |
# | ---------- | ----------- |
# | Curador    | 0.1         |
# | Exegeta    | 0.2         |
# | Integrador | 0.4         |
# | Refinador  | 0.3         |
# | Crítico    | 0.0         |
# ============================
# AGENTE CURADOR
# =========================
def agente_curador(contexto, run_id, iteracao):
    resultados = buscar_versiculos(contexto["pergunta"])
    memorias = buscar_memoria(contexto["pergunta"], tipo="curador")
    # memorias = ""

    prompt = f"""
    PERGUNTA:
    {contexto['pergunta']}

    TEXTOS RECUPERADOS:
    {resultados}

    MEMÓRIAS DE SELEÇÕES ANTERIORES:
    {memorias}    

    TAREFA:
    Selecione até 5 textos bíblicos mais relevantes considerando:
    - Similaridade com a pergunta
    - Profundidade existencial
    - Conexão com memórias anteriores

    IMPORTANTE:
    - Priorize a similaridade com a pergunta
    - NÃO copie as memórias diretamente, use as somente como referência de qualidade

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
    # memorias = ""

    prompt = f"""
    BASE:
    {analise}

    PERGUNTA:
    {contexto['pergunta']}

    MEMÓRIAS DE SELEÇÕES ANTERIORES:
    {memorias}
        
    TAREFA:
    Gere uma resposta existencial e pastoral:
    - Clara
    - Profunda
    - Conectada à experiência humana
    - Busque originalidade com consistência
    
    IMPORTANTE:
    - Priorize a similaridade com a pergunta
    - NÃO copie as memórias diretamente, use as somente como referência de qualidade

    Inclua as referências bíblicas após a conclusão
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