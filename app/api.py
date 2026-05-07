# app/api.py
import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

# Importa as funções do pipeline e do banco de dados
# Certifique-se de que o diretório 'app' está no sys.path ou use importações relativas
from .app import pipeline
from .storage import init_db, aplicar_decay

# -----------------------------------------------------------
# 1. Modelos Pydantic para Requisição e Resposta
# -----------------------------------------------------------
class PerguntaRequest(BaseModel):
    """
    Modelo para validar a requisição do usuário.
    A pergunta é obrigatória e deve ter no máximo 1000 caracteres.
    """
    pergunta: str = Field(
        ...,
        max_length=1000,
        title="Pergunta existencial",
        description="A pergunta que será analisada pelo pipeline de agentes.",
        example="Por que eu sinto vazio mesmo tendo tudo?"
    )

class RespostaPipeline(BaseModel):
    """
    Modelo para estruturar a resposta da API.
    Inclui a pergunta original, a resposta final do pipeline e um indicador de status.
    """
    pergunta: str
    resposta: str
    status: str = "sucesso"

# -----------------------------------------------------------
# 2. Gerenciamento do Ciclo de Vida (Lifespan)
# -----------------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gerencia a inicialização e finalização dos recursos.
    Inicializa o banco de dados na partida e aplica o decay na parada.
    """
    # Ações na inicialização do servidor
    print("Inicializando banco de dados...")
    init_db()
    print("API pronta para receber requisições.")
    yield
    # Ações na finalização do servidor
    print("Aplicando decay e finalizando...")
    aplicar_decay()
    print("API encerrada.")

# -----------------------------------------------------------
# 3. Criação da Aplicação FastAPI
# -----------------------------------------------------------
app = FastAPI(
    title="PoC Bíblia IA - API",
    description="API para interagir com a comunidade de agentes de IA especializados em reflexão existencial baseada na Bíblia.",
    version="0.3.0",
    lifespan=lifespan
)

# -----------------------------------------------------------
# 4. Endpoints da API
# -----------------------------------------------------------
@app.get("/health", tags=["Health"])
async def health_check():
    """
    Endpoint para verificar se a API está funcionando.
    """
    return {"status": "ok", "message": "PoC Bíblia IA API está operacional."}

@app.post("/pipeline", response_model=RespostaPipeline, tags=["Pipeline"])
async def executar_pipeline(request: PerguntaRequest):
    """
    Endpoint principal que executa o pipeline multiagente sobre a pergunta fornecida.
    """
    try:
        # Chama a função pipeline do arquivo app.py
        resposta_final = pipeline(request.pergunta)
        return RespostaPipeline(
            pergunta=request.pergunta,
            resposta=resposta_final
        )
    except Exception as e:
        # Em caso de erro, retorna um HTTP 500 com detalhes.
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao processar a pergunta: {str(e)}"
        )