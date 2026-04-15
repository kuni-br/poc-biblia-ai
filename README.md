# 📖 PoC Bíblia IA - v0.3

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Architecture: Multi-Agent](https://img.shields.io/badge/Architecture-Multi--Agent-green.svg)](https://en.wikipedia.org/wiki/Multi-agent_system)
[![LLM: Ollama/DeepSeek](https://img.shields.io/badge/LLM-Ollama%2FDeepSeek-orange.svg)](https://ollama.ai/)

## 🧠 Visão Geral

Esta **Proof of Concept (PoC)** implementa uma comunidade de agentes de IA especializados em **reflexão existencial baseada na Bíblia**. O sistema simula um processo interpretativo inspirado em tradições teológicas, combinando:

- **Arquitetura multiagente** com especialização por função
- **Memória semântica adaptativa** com aprendizado contínuo
- **RAG (Retrieval-Augmented Generation)** para busca contextual
- **Avaliação automática** e refinamento iterativo

> **Nota importante**: Este é um projeto experimental para estudo de IA aplicada à teologia. Não substitui estudo bíblico tradicional ou aconselhamento pastoral qualificado.

## 📑 Índice

- [🚀 Começando Rápido](#-começando-rápido)
- [📋 Pré-requisitos](#-pré-requisitos)
- [⚙️ Instalação](#️-instalação)
- [🔧 Configuração](#-configuração)
- [🏗️ Arquitetura](#️-arquitetura)
- [🤖 Agentes](#-agentes)
- [📁 Estrutura do Projeto](#-estrutura-do-projeto)
- [🧪 Como Usar](#-como-usar)
- [📊 Memória e Aprendizado](#-memória-e-aprendizado)
- [🔮 Próximos Passos](#-próximos-passos)
- [📝 Licença](#-licença)

## 🚀 Começando Rápido

```bash
# 1. Clone o repositório
git clone <repo-url>
cd poc-biblia-ai

# 2. Instale dependências
pip install -r requirements.txt

# 3. Baixe e prepare os dados da Bíblia
# O projeto usa a Bíblia Almeida Revisada Imprensa Bíblica (AA) em formato JSON
# Faça download do arquivo: https://github.com/thiagobodruk/biblia/blob/master/json/aa.json
# Salve como: data/biblia_ara.json
# Em seguida, execute a ingestão:
python scripts/ingest_biblia.py

# 4. Configure o ambiente
cp .env.example .env
# Edite .env com suas chaves API

# 5. Execute o sistema
python app/main.py
```

## 📋 Pré-requisitos

- **Python 3.8+** com pip
- **Ollama** (opcional, para execução local) - [Instalação](https://ollama.ai/)
- **Conta DeepSeek** (opcional, para API cloud) - [Registro](https://platform.deepseek.com/)
- **~2GB RAM** livre para modelos locais
- **SQLite3** (incluído no Python)
- **Dados da Bíblia**: Arquivo `aa.json` do repositório [thiagobodruk/biblia](https://github.com/thiagobodruk/biblia)

## ⚙️ Instalação

### 1. Ambiente Virtual (Recomendado)

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
```

### 2. Dependências Python

```bash
pip install -r requirements.txt
```

> **Nota**: Se `requirements.txt` estiver vazio, instale manualmente:
> ```bash
> pip install sentence-transformers numpy requests openai python-dotenv
> ```

### 3. Obtenha os Dados da Bíblia

```bash
# Crie o diretório data se não existir
mkdir -p data

# Baixe a Bíblia Almeida Revisada Imprensa Bíblica (AA) em formato JSON
# Opção 1: Download manual
# Acesse: https://github.com/thiagobodruk/biblia/blob/master/json/aa.json
# Salve como: data/biblia_ara.json

# Opção 2: Usando curl (se disponível)
curl -L "https://raw.githubusercontent.com/thiagobodruk/biblia/master/json/aa.json" -o "data/biblia_ara.json"
```

### 4. Modelo Ollama (Opcional)

```bash
# Instale o Ollama primeiro (https://ollama.ai/)
ollama pull llama3:8b-instruct-q4_K_M
```

## 🔧 Configuração

### Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
# Escolha o provedor: "ollama" ou "deepseek"
LLM_PROVIDER=deepseek

# Configuração DeepSeek (se usar)
DEEPSEEK_API_KEY=sua_chave_aqui
DEEPSEEK_MODEL=deepseek-chat

# Configuração Ollama (se usar)
OLLAMA_URL=http://localhost:11434/api/generate
OLLAMA_MODEL=llama3:8b-instruct-q4_K_M
```

### Ingestão da Bíblia

Após obter o arquivo data/biblia_ara.json (baixado do repositório thiagobodruk/biblia), execute:

```bash
# Processa a Bíblia e gera embeddings para busca semântica
python scripts/ingest_biblia.py
```

Isso criará:
- `data/biblia_ara_index.json` (embeddings para busca semântica)
- A partir de `data/biblia_ara.json` (deve existir previamente)

**Nota sobre os dados**: O projeto usa a **Bíblia Almeida Revisada Imprensa Bíblica (AA)** obtida do repositório [thiagobodruk/biblia](https://github.com/thiagobodruk/biblia/). Esta é uma tradução protestante em português amplamente utilizada no Brasil.

## 🏗️ Arquitetura

### Diagrama do Fluxo

```text
┌─────────────────┐
│   PERGUNTA      │
│   Existencial   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│    CURADOR      │
│  (RAG + Memória)│
│  Seleciona textos│
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│    EXEGETA      │
│  Análise histórica│
│  e teológica    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   INTEGRADOR    │
│  (Memória)      │
│  Resposta       │
│  existencial    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│    CRÍTICO      │
│  Avaliação JSON │
│  (0-30 pontos)  │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
 APROVAR   REVISAR
    │         │
    │         ▼
    │   ┌───────────┐
    │   │ REFINADOR │
    │   │ Melhora   │
    │   │ resposta  │
    │   └─────┬─────┘
    │         │
    └─────┬───┘
          │
          ▼
   RESPOSTA FINAL
```

### Banco de Dados

O sistema usa SQLite com três tabelas principais:

1. **`runs`**: Logs completos de execução
2. **`memoria`**: Memória semântica dos agentes (aprendizado)
3. **`versiculos`**: Estatísticas de uso dos textos bíblicos

## 🤖 Agentes

### 1. **Curador** (`temperature=0.1`)
- **Função**: Seleciona textos bíblicos relevantes
- **Técnicas**: RAG + similaridade semântica + memória
- **Entrada**: Pergunta do usuário
- **Saída**: Até 5 textos bíblicos com justificativa

### 2. **Exegeta** (`temperature=0.2`)
- **Função**: Análise contextual profunda
- **Aspectos**: Contexto histórico, significado original, conflitos humanos
- **Entrada**: Textos selecionados pelo Curador
- **Saída**: Análise exegética detalhada

### 3. **Integrador** (`temperature=0.4`)
- **Função**: Síntese existencial
- **Características**: Resposta pastoral, conexão humana, originalidade
- **Entrada**: Análise do Exegeta + memória semântica
- **Saída**: Resposta existencial completa

### 4. **Crítico** (`temperature=0.0`)
- **Função**: Avaliação estruturada
- **Critérios**:
  - Fidelidade bíblica (0-10)
  - Clareza (0-10)
  - Profundidade (0-10)
- **Saída**: JSON com score total (0-30) e decisão (APROVAR/REVISAR)

### 5. **Refinador** (`temperature=0.3`)
- **Função**: Melhoria iterativa
- **Acionamento**: Quando o Crítico retorna "REVISAR"
- **Entrada**: Resposta original + feedback do Crítico
- **Saída**: Resposta refinada

## 📁 Estrutura do Projeto

```text
poc-biblia-ai/
├── app/                    # Código principal
│   ├── agents.py          # Definição dos agentes
│   ├── app.py             # Pipeline de orquestração
│   ├── main.py            # Ponto de entrada com perguntas de exemplo
│   ├── storage.py         # Banco SQLite + memória semântica
│   ├── rag.py             # Busca RAG em embeddings
│   └── llm_client.py      # Cliente LLM (Ollama/DeepSeek)
│
├── scripts/               # Scripts utilitários
│   ├── ingest_biblia.py   # Processamento da Bíblia
│   ├── convert_biblia.py  # Conversão de formatos
│   ├── csv_to_html.py     # Exportação HTML
│   └── csv_to_pdf.py      # Exportação PDF
│
├── data/                  # Dados e persistência
│   ├── biblia_ara.json    # Bíblia Almeida Revisada Imprensa Bíblica (AA) - baixada de thiagobodruk/biblia
│   ├── biblia_ara_index.json  # Embeddings para RAG
│   ├── logs.db            # Banco SQLite principal
│   └── logs*.db           # Backups de logs
│
├── .env.example           # Template de configuração
├── requirements.txt       # Dependências Python
├── LICENSE               # Licença MIT
├── README.md             # Documentação original
└── newREADME.md          # Esta documentação melhorada
```

## 🧪 Como Usar

### Execução Básica

```bash
python app/main.py
```

O sistema executará automaticamente 40 perguntas filosófico existenciais de exemplo.

### Perguntas Personalizadas

Edite `app/main.py` e modifique a lista `perguntas`:

```python
# Em app/main.py
perguntas = [
    "Sua pergunta existencial aqui?",
    # ... outras perguntas
]
```

### Exemplos de Perguntas Incluídas

A aplicação inclui 40 perguntas filosófico exitenciais, como:

1. "Por que eu sinto vazio mesmo tendo tudo?"
2. "Como justificar a exigência de perdoar o imperdoável?"
3. "Se o tempo é uma dimensão irreversível, em que sentido o 'eu' que promete hoje é o mesmo que deve cumprir amanhã?"
4. "O que significa 'dar a vida por algo'?"
5. "Como distinguir entre humildade autêntica e humilhação imposta?"

### Monitoramento

Acesse os logs em tempo real:

```bash
# Use um cliente SQLite
sqlite3 data/logs.db

-- Consultas úteis
SELECT * FROM runs ORDER BY timestamp DESC LIMIT 5;
SELECT agente, COUNT(*) FROM runs GROUP BY agente;
SELECT score, decisao FROM runs WHERE raw_json LIKE '%decisao%';
```

## 📊 Memória e Aprendizado

### Sistema de Memória Semântica

O sistema possui memória separada por tipo de agente:

| Tipo | Conteúdo | Uso |
|------|----------|-----|
| `curador` | Textos selecionados | Melhorar seleção futura |
| `integrador` | Respostas existenciais | Melhorar qualidade das respostas |

### Ranking Híbrido

As memórias são classificadas por:
```python
score_final = (
    similaridade_semantica * 0.5 +
    score_historico * 0.006 +
    peso * 0.2 +
    fator_recencia * 0.05 +
    fator_frequencia * 0.05
)
```

### Aprendizado Contínuo

1. **Reforço Positivo**: Memórias associadas a respostas bem avaliadas (`score_total >= 24`) são fortalecidas
2. **Decay (Esquecimento)**: Memórias não utilizadas perdem peso ao longo do tempo
3. **Limpeza Automática**: Memórias com peso muito baixo (`< 0.2`) são removidas

## 🔮 Próximos Passos

### Melhorias Planejadas

- [ ] **Interface Web**: Dashboard para interação e visualização
- [ ] **Mais Traduções**: Suporte a outras versões da Bíblia
- [ ] **API REST**: Endpoints para integração com outros sistemas

### Melhorias Técnicas Sugeridas

1. **Testes Unitários**: Cobertura para agentes e pipeline
2. **Dockerização**: Container para fácil implantação
3. **Monitoramento Avançado**: Métricas de performance e qualidade
4. **Cache de Embeddings**: Otimização de performance
5. **Sistema de Plugins**: Extensibilidade para novos agentes

### Roadmap de Versões

- **v0.4**: Interface web básica + mais traduções bíblicas
- **v0.5**: Sistema de plugins + API REST
- **v1.0**: Versão estável com documentação completa

## ⚠️ Considerações Éticas e Limitações

### Limitações Técnicas

1. **Dependência de LLMs**: As respostas refletem os vieses e limitações dos modelos usados
2. **Contexto Cultural**: Análises podem não considerar adequadamente contextos culturais específicos
3. **Precisão Teológica**: O sistema é uma PoC e não substitui estudo teológico aprofundado
4. **Interpretação Literal**: Pode haver dificuldade com linguagem figurativa ou poética

### Uso Responsável

- **Para estudo e reflexão**, não para aconselhamento pastoral
- **Complementar**, não substituto de comunidades religiosas reais
- **Transparência**: Sempre indicar que as respostas são geradas por IA
- **Supervisão Humana**: Respostas devem ser revisadas por especialistas quando usado em contextos sensíveis

## 👥 Contribuindo

Contribuições são bem-vindas! Por favor:

1. Fork o repositório
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

### Áreas que Precisam de Contribuição

- Documentação
- Testes
- Novos agentes especializados
- Interface de usuário
- Otimizações de performance

## 📝 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

```
MIT License

Copyright (c) 2026 kuni-br

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

## 🙏 Agradecimentos

- **Comunidade Ollama** pelos modelos LLM acessíveis
- **DeepSeek** pela API generosa
- **SentenceTransformers** pelos embeddings de qualidade
- **Thiago Bodruk** pelo texto bíblico da Almeida Revisada Imprensa Bíblica

---

**Nota**: Este é um projeto em desenvolvimento ativo. Issues, sugestões e contribuições são muito apreciadas!

*"Porque a palavra de Deus é viva, e eficaz, e mais cortante do que qualquer espada de dois gumes, e penetra até ao ponto de dividir alma e espírito, juntas e medulas, e é apta para discernir os pensamentos e propósitos do coração." - Hebreus 4:12*