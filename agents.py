from app import chamar_llm
from prompts import *
from storage import save_output
import re

def extrair_resposta_final(texto):
    match = re.search(r"\[RESPOSTA FINAL\](.*)", texto, re.DOTALL)
    return match.group(1).strip() if match else texto


def pipeline(pergunta):

    # 1. Curador
    curador = chamar_llm(curador_prompt(pergunta))
    save_output(pergunta, "curador", curador)

    # 2. Exegeta (fonte de verdade)
    exegeta = chamar_llm(exegeta_prompt(curador))
    save_output(pergunta, "exegeta", exegeta)

    # 3. Integrador (limitado ao exegeta)
    integrador = chamar_llm(integrador_prompt(exegeta, pergunta))
    save_output(pergunta, "integrador", integrador)

    # 4. Crítico (valida + corrige + score)
    critico = chamar_llm(critico_prompt(integrador))
    save_output(pergunta, "critico", critico)

    resposta_final = extrair_resposta_final(critico)

    return resposta_final