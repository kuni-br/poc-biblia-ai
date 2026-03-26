# 📖 PoC Bíblia IA - Multiagente (v0.2)

Uma prova de conceito de um sistema multiagente para gerar **reflexões existenciais baseadas na Bíblia**, utilizando LLM local via Ollama, RAG semântico e pipeline iterativo com avaliação automática.

---

## 🎯 Objetivo

Construir uma comunidade de agentes de IA capazes de:

* Interpretar textos bíblicos
* Gerar reflexões existenciais profundas
* Avaliar a qualidade das respostas
* Refinar iterativamente o conteúdo

Inspirado na autoavaliação de personagens bíblicos como Davi, Paulo e Pedro.

---

## 🧠 Arquitetura

Pipeline multiagente com loop de refinamento:

```
Curador → Exegeta → Integrador → Crítico → Refinador
                                 ↑         ↓
                           (loop iterativo)
```

---

## 🤖 Agentes

### 🔎 Curador

* Recupera versículos via RAG
* Seleciona os mais relevantes

### 📜 Exegeta

* Analisa o contexto histórico e teológico
* Identifica conflitos humanos no texto

### 🧩 Integrador

* Gera resposta existencial
* Conecta Bíblia com experiência humana

### ⚖️ Crítico (JSON)

* Avalia a resposta em:

  * Fidelidade bíblica
  * Clareza
  * Profundidade
* Retorna saída estruturada em JSON

### 🔧 Refinador

* Reescreve a resposta com base no feedback
* Melhora progressivamente a qualidade

---

## 🔁 Loop Inteligente

O sistema executa até `MAX_ITERACOES` (default: 3):

* Se `decisao == APROVAR` → encerra
* Se `score_total >= 24` → aceita resposta
* Caso contrário → refinamento contínuo

---

## 📦 Estrutura do Projeto

```
.
├── agents.py        # Definição dos agentes
├── app.py           # Pipeline principal
├── main.py          # Execução da aplicação
├── rag.py           # Busca semântica (RAG)
├── storage.py       # Persistência SQLite
├── data/
│   ├── biblia_ara_index.json
│   └── logs.db
```

---

## 🧪 Tecnologias Utilizadas

* 🧠 LLM local via Ollama (`llama3`)
* 🔎 Sentence Transformers (`all-MiniLM-L6-v2`)
* 🧮 NumPy (similaridade vetorial)
* 🗄 SQLite (persistência)
* 🐍 Python

---

## 🔍 RAG (Retrieval-Augmented Generation)

O sistema utiliza embeddings semânticos para recuperar versículos relevantes:

* Modelo: `all-MiniLM-L6-v2`
* Similaridade: **cosine similarity**
* Top-K: 5 versículos

---

## 📊 Avaliação Estruturada (Crítico)

Exemplo de saída do agente crítico:

```json
{
  "fidelidade": 8,
  "clareza": 9,
  "profundidade": 7,
  "score_total": 24,
  "feedback": "Boa conexão com o texto bíblico, mas pode aprofundar a aplicação pessoal.",
  "decisao": "REVISAR"
}
```

---

## 💾 Persistência

Cada execução é registrada em SQLite (`data/logs.db`):

Tabela: `runs`

Campos:

* `run_id`
* `iteracao`
* `agente`
* `pergunta`
* `entrada`
* `saida`
* `score`
* `feedback`
* `raw_json`

---

## 🚀 Como executar

### 1. Instalar dependências

```bash
pip install sentence-transformers numpy requests
```

---

### 2. Iniciar o Ollama

```bash
ollama run llama3
```

---

### 3. Executar o projeto

```bash
python main.py
```

---

## 🧪 Exemplos de Perguntas

```python
perguntas = [
    "Por que reconhecer meus erros é tão difícil?",
    "Por que o ser humano falha mesmo querendo acertar?",
    "Como lidar com uma culpa profunda?",
    "Qual o sentido do sofrimento?"
]
```

---

## 🔧 Melhorias da versão 0.2

### ✅ Arquitetura

* Introdução de loop iterativo real
* Separação clara de responsabilidades entre agentes

### ✅ Crítico estruturado

* Saída em JSON (eliminando parsing frágil)
* Validação de estrutura

### ✅ Robustez

* Fallback para extração de JSON
* Tratamento de erro no parsing

### ✅ RAG aprimorado

* Uso correto de cosine similarity
* Melhor ranking semântico

### ✅ Persistência evoluída

* Armazenamento de JSON bruto (`raw_json`)
* Suporte a análise posterior

---

## ⚠️ Limitações atuais

* Dependência de LLM local (latência)
* Possível inconsistência no JSON do crítico
* Sem validação teológica profunda (ainda)
* Sem memória entre execuções

---

## 🔮 Próximos passos (v0.3+)

* 📚 Agente baseado em personagens bíblicos (Davi, Paulo, etc.)
* 🧠 Memória semântica entre execuções
* 📊 Dashboard de avaliação dos agentes
* 🔍 Validação automática de referências bíblicas
* 🎯 Ranking de respostas por qualidade

---

## 📌 Conclusão

Esta PoC demonstra como um sistema multiagente pode:

* Interpretar textos complexos
* Gerar reflexão existencial
* Avaliar a si mesmo
* Evoluir iterativamente

Servindo como base para sistemas mais avançados de IA aplicada à teologia e filosofia.

---

## 👨‍💻 Autor

Projeto desenvolvido por Marcos Kuniyoshi

---

## 📄 Licença

MIT

---