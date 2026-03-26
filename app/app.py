from agents import *
import uuid

MAX_ITERACOES = 3

def pipeline(pergunta):
    run_id = str(uuid.uuid4())

    contexto = {
        "pergunta": pergunta,
        "historico": []
    }

    resposta_atual = None

    # primeira iteração completa
    for i in range(MAX_ITERACOES):
        print(f"\n--- Iteração {i+1} ---")

        if i == 0:
            curador = agente_curador(contexto, run_id, i)
            exegeta = agente_exegeta(curador, contexto, run_id, i)
            resposta_atual = agente_integrador(exegeta, contexto, run_id, i)
        # refinamentos subsequentes            
        else:
            resposta_atual = agente_refinador(
                resposta_atual,
                contexto["historico"][-1]["critico"]["feedback"],
                contexto,
                run_id,
                i
            )

        critico = agente_critico(resposta_atual, contexto, run_id, i)

        contexto["historico"].append({
            "resposta": resposta_atual,
            "critico": critico
        })

        # decisão inteligente
        if critico.get("decisao") == "APROVAR":
            return resposta_atual

        # fallback por score
        if critico.get("score_total", 0) >= 24:
            return resposta_atual

    return resposta_atual