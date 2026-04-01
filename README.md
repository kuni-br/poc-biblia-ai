# 📖 PoC Bíblia IA - v0.3

## 🧠 Visão Geral

Esta Proof of Concept (PoC) implementa uma **comunidade de agentes de IA especializados em reflexão existencial baseada na Bíblia**, com arquitetura multiagente, memória semântica adaptativa e avaliação automática.

O sistema simula um processo interpretativo inspirado em tradições teológicas:

* Seleção de textos (curadoria)
* Análise exegética
* Síntese existencial
* Avaliação crítica
* Refinamento iterativo

---

## 🚀 Novidades da versão 0.3

### 🧠 Memória Semântica Evolutiva

* Memória separada por tipo:

  * `curador` → seleção de versículos
  * `integrador` → respostas existenciais
* Busca híbrida com:

  * Similaridade semântica
  * Score do agente crítico
  * Peso dinâmico (reforço)
  * Recência
  * Frequência de uso

---

### 🔁 Aprendizado Contínuo

* **Reforço positivo**:

  * Memórias associadas a respostas bem avaliadas são fortalecidas
* **Esquecimento (decay)**:

  * Memórias não utilizadas perdem relevância ao longo do tempo
* **Limpeza automática**:

  * Remoção de memórias fracas

---

### 🤖 Arquitetura Multiagente

| Agente     | Função                                 |
| ---------- | -------------------------------------- |
| Curador    | Seleciona textos bíblicos relevantes   |
| Exegeta    | Analisa contexto histórico e teológico |
| Integrador | Gera resposta existencial              |
| Crítico    | Avalia qualidade (JSON estruturado)    |
| Refinador  | Melhora respostas com base no feedback |

---

### 📊 Avaliação Automatizada

O agente crítico avalia:

* Fidelidade bíblica
* Clareza
* Profundidade

E retorna:

```json
{
  "score_total": 0-30,
  "decisao": "APROVAR" ou "REVISAR"
}
```

---

### 🧩 RAG (Retrieval-Augmented Generation)

* Baseado em embeddings pré-processados (JSON)
* Busca por similaridade semântica
* Ranking híbrido com densidade existencial

---

## 🏗️ Arquitetura

```text
Pergunta
  ↓
Curador (RAG + memória)
  ↓
Exegeta
  ↓
Integrador (memória)
  ↓
Crítico (avaliação)
  ↓
Refinador (se necessário)
```

---

## 📁 Estrutura do Projeto

```text
poc-biblia-ai/
│
├── agents.py          # Lógica dos agentes
├── app.py             # Orquestração do pipeline
├── main.py            # Ponto de entrada
├── storage.py         # Banco + memória semântica
├── rag.py             # Busca de versículos (JSON)
├── llm_client.py      # Abstração de LLM (Ollama/OpenAI)
│
├── data/
│   ├── biblia_ara_index.json
│   └── logs.db
│
├── requirements.txt
└── README.md
```

---

## ⚙️ Configuração

### 1. Instalar dependências

```bash
pip install -r requirements.txt
```

---

### 2. Configurar variáveis de ambiente

Crie um arquivo `.env`:

```env
LLM_PROVIDER=ollama
OPENAI_API_KEY=your_key_here
```

---

### 3. Rodar o sistema

```bash
python main.py
```

---

## 🤖 Modelos suportados

### 🟢 Ollama (local)

* Modelo padrão:

  ```
  llama3:8b-instruct-q4_K_M
  ```

---

### 🔵 OpenAI (opcional)

* Modelo:

  ```
  gpt-4.1-mini
  ```

Trocar via `.env`:

```env
LLM_PROVIDER=openai
```

---

## 🧠 Memória Semântica

### Estrutura

```text
tipo | pergunta | conteudo | embedding | score | peso | vezes_usada | ultimo_uso
```

---

### Ranking híbrido

```text
score_final =
  similaridade +
  score +
  peso +
  recência +
  frequência
```

---

### Tipos de memória

| Tipo       | Uso                             |
| ---------- | ------------------------------- |
| curador    | melhorar seleção de versículos  |
| integrador | melhorar respostas existenciais |

---

## 🔁 Aprendizado

### ✔ Reforço

* Aplicado quando:

  ```
  score_total >= 24
  ```
* Aumenta o peso das memórias relevantes

---

### 🗑️ Decay

* Reduz peso com o tempo
* Remove memórias fracas

---

## 📊 Logs e Observabilidade

Tabela `runs` armazena:

* entrada
* saída por agente
* score
* feedback

---

## 🧪 Exemplo de uso

```text
Pergunta:
"Por que eu sinto vazio mesmo tendo tudo?"
```

Saída:

* textos bíblicos relevantes
* análise exegética
* resposta existencial profunda
* avaliação automática
* refinamento (se necessário)

---

## 🎯 Objetivo da PoC

Criar um sistema que:

* interpreta a Bíblia de forma contextual
* responde questões existenciais humanas
* aprende com o tempo
* evolui qualitativamente

---

## 🔮 Próximos passos

* Ranking por densidade existencial avançado
* Clusterização de temas (culpa, propósito, sofrimento)
* Avaliação comparativa entre modelos (A/B test)
* Interface web
* Uso de banco vetorial

---

## 🧠 Insight central

Este projeto não é apenas um chatbot.

É um sistema que busca simular:

> uma tradição interpretativa que aprende, refina e amadurece com o tempo.

---

## 📌 Versão

```
v0.3 — Memória adaptativa + aprendizado contínuo
```

---

## 👨‍💻 Autor

Projeto experimental para estudo de:

* Multiagentes
* RAG
* Memória semântica
* IA aplicada à teologia

---
