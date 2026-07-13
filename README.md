# AI News Aggregator

> Agregador de notícias, papers acadêmicos e repositórios sobre Inteligência Artificial de múltiplas fontes confiáveis.

[![MCP](https://img.shields.io/badge/MCP-Enabled-blue)](https://modelcontextprotocol.io)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-green)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.10+-orange)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)
[![Deploy](https://img.shields.io/badge/Deploy-Render-purple)](https://render.com)
[![Status](https://img.shields.io/badge/Status-Active-success)]()

**Live API:** [mcp-ai-news.onrender.com](https://mcp-ai-news.onrender.com/docs)

---

## Índice

- [Sobre](#sobre)
- [Features](#features)
- [Fontes de Dados](#fontes-de-dados)
- [Instalação](#instalação)
  - [MCP Server (Local)](#mcp-server-local)
  - [REST API (Deploy)](#rest-api-deploy)
- [Uso](#uso)
  - [Claude Code/Desktop](#claude-codedesktop)
  - [REST API](#rest-api)
  - [Claude Web](#claude-web)
- [API Reference](#api-reference)
- [Cache](#cache)
- [Deploy](#deploy)
- [Desenvolvimento](#desenvolvimento)
- [Performance](#performance)
- [Troubleshooting](#troubleshooting)
- [Contribuindo](#contribuindo)
- [Autor](#autor)
- [Licença](#licença)

---

## Sobre

Este projeto oferece **duas formas** de acessar conteúdo sobre IA:

1. **MCP Server** - Integração nativa com Claude Code/Desktop via protocolo MCP
2. **REST API** - API HTTP pública para acesso de qualquer aplicação

**Agregamos de 10 fontes:**
- 8 blogs especializados (OpenAI, Anthropic, Google AI, DeepMind, etc.)
- ArXiv papers (5 categorias: cs.AI, cs.LG, cs.CL, cs.CV, stat.ML)
- GitHub trending repositories (AI/ML)

**~180+ itens** agregados em tempo real com cache inteligente de 15 minutos.

---

## Features

- 10 fontes confiáveis de conteúdo sobre IA
- Filtro temporal configurável (1-90 dias)
- Busca por palavra-chave em títulos e resumos
- Cache em memória (15 min) para performance
- MCP Server para Claude Code/Desktop
- REST API com documentação Swagger/ReDoc
- CORS habilitado para acesso público
- Deploy gratuito no Render

---

## Fontes de Dados

### Blogs RSS (8 fontes)

| Blog | Cobertura |
|------|-----------|
| **OpenAI** | GPT, ChatGPT, DALL-E |
| **Anthropic** | Claude, Constitutional AI |
| **Google AI** | Gemini, Bard, Research |
| **DeepMind** | AlphaFold, AlphaGo |
| **Hugging Face** | Open-source models |
| **MIT Tech Review** | Análises profundas |
| **TechCrunch AI** | Startups, mercado |
| **The Verge AI** | Consumer tech |

### Papers Acadêmicos (ArXiv)

Categorias: `cs.AI`, `cs.LG`, `cs.CL`, `cs.CV`, `stat.ML`

### Repositórios (GitHub)

Topics: `artificial-intelligence`, `machine-learning`, `deep-learning`, `llm`, `transformers`

---

## Instalação

### MCP Server (Local)

Para uso com Claude Code ou Claude Desktop:

```bash
# 1. Clone o repositório
git clone https://github.com/LauraMattz/mcp_ai_news.git
cd mcp_ai_news

# 2. Instale dependências
pip install -r requirements.txt

# 3. Configure .mcp.json na raiz do projeto
```

**`.mcp.json`:**
```json
{
  "mcpServers": {
    "ai-news": {
      "command": "python",
      "args": ["server.py"]
    }
  }
}
```

**Recarregue:** `Ctrl+Shift+P` → "Developer: Reload Window"

#### Claude Desktop

Edite `claude_desktop_config.json`:
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
- **Mac/Linux:** `~/.config/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "ai-news": {
      "command": "python",
      "args": ["/caminho/completo/para/server.py"]
    }
  }
}
```

### REST API (Deploy)

```bash
# Rodar localmente
python api.py

# Acessar documentação
http://localhost:8000/docs
```

---

## Uso

### Claude Code/Desktop

Após configuração do MCP, use comandos naturais:

```
"Liste as últimas notícias de IA"
"Busque conteúdo sobre transformers"
"Mostre papers do ArXiv sobre computer vision"
"Repositórios trending de machine learning"
```

**5 Tools MCP disponíveis:**
- `list_ai_news` - Todas as fontes agregadas
- `search_ai_content` - Busca por palavra-chave
- `list_arxiv_papers` - Papers acadêmicos
- `list_github_trending` - Repos populares
- `list_sources` - Fontes configuradas

### REST API

#### Endpoints

| Endpoint | Descrição | Cache |
|----------|-----------|-------|
| `GET /` | Info da API | - |
| `GET /health` | Health check | - |
| `GET /news` | Todas as notícias | 15 min |
| `GET /search?q=keyword` | Busca por palavra-chave | 15 min |
| `GET /papers` | Papers do ArXiv | 15 min |
| `GET /github` | Repos trending | 15 min |
| `GET /sources` | Lista fontes | - |
| `GET /docs` | Documentação Swagger | - |

#### Exemplos de uso

```bash
# Notícias gerais (últimos 7 dias, limite 20)
curl https://mcp-ai-news.onrender.com/news?days=7&limit=20

# Buscar por "GPT"
curl https://mcp-ai-news.onrender.com/search?q=GPT&days=14

# Papers recentes (3 dias, máximo 10)
curl https://mcp-ai-news.onrender.com/papers?days=3&max_results=10

# Repos trending (última semana)
curl https://mcp-ai-news.onrender.com/github?days=7&max_results=10

# Listar fontes configuradas
curl https://mcp-ai-news.onrender.com/sources
```

### Claude Web

Cole URLs diretamente nos prompts:

```
Acesse https://mcp-ai-news.onrender.com/news?days=7&limit=15
e me mostre as principais notícias sobre IA da última semana
```

```
Busque em https://mcp-ai-news.onrender.com/search?q=transformer
e resuma os avanços em modelos transformer
```

---

## API Reference

### `GET /news`

Lista todas as notícias agregadas.

**Query Parameters:**
- `days` (int, 1-90): Dias retroativos (default: 14)
- `include_papers` (bool): Incluir ArXiv (default: true)
- `include_github` (bool): Incluir GitHub (default: true)
- `limit` (int, 1-200): Limitar resultados (opcional)

**Response:**
```json
{
  "total": 103,
  "dias": 7,
  "fontes": {
    "OpenAI Blog": 12,
    "ArXiv": 50,
    "GitHub": 30,
    ...
  },
  "resultados": [...]
}
```

### `GET /search`

Busca por palavra-chave.

**Query Parameters:**
- `q` (string, min 2): Palavra-chave (obrigatório)
- `days` (int, 1-90): Dias retroativos (default: 14)

### `GET /papers`

Lista papers do ArXiv.

**Query Parameters:**
- `days` (int, 1-90): Dias retroativos (default: 14)
- `max_results` (int, 1-100): Máximo papers (default: 50)

### `GET /github`

Lista repos trending.

**Query Parameters:**
- `days` (int, 1-90): Dias retroativos (default: 14)
- `max_results` (int, 1-50): Máximo repos (default: 30)

---

## Cache

Sistema de cache em memória para performance:

- **TTL:** 15 minutos
- **Escopo:** Por endpoint + parâmetros
- **Benefício:** Respostas <100ms (vs 10-15s)
- **Atualização:** Automática após expiração

**Chaves de cache:**
- `/news`: `news_{days}_{papers}_{github}_{limit}`
- `/search`: `search_{keyword}_{days}`
- `/papers`: `papers_{days}_{max_results}`
- `/github`: `github_{days}_{max_results}`

---

## Deploy

### Render (Gratuito)

1. Fork este repositório
2. Criar conta: [render.com](https://render.com)
3. **New Web Service** → conectar GitHub
4. Render detecta `render.yaml` automaticamente
5. Deploy em ~5 minutos

**Build:** `pip install -r requirements.txt`
**Start:** `uvicorn api:app --host 0.0.0.0 --port $PORT`

**Free tier:**
- 750h/mês
- Dorme após 15 min inatividade
- 512 MB RAM

### Alternativas

- **Railway:** 500h/mês ou $5 crédito
- **Fly.io:** $5 crédito/mês
- **Docker:** Use `render.yaml` como referência

---

## Desenvolvimento

### Adicionar nova fonte RSS

```python
# Em server.py e api.py
FONTES_RSS["nova_fonte"] = {
    "nome": "Nome da Fonte",
    "url": "https://fonte.com/rss.xml",
    "ativa": True
}
```

### Adicionar categoria ArXiv

```python
# Em server.py e api.py
ARXIV_CATEGORIAS = ["cs.AI", "cs.LG", "cs.CL", "cs.CV", "stat.ML", "cs.RO"]
```

### Testar

```bash
# MCP Server
python server.py

# MCP Inspector (interface web)
npx @modelcontextprotocol/inspector python server.py
# Acesse: http://localhost:6274

# REST API
python api.py
# Acesse: http://localhost:8000/docs
```

### Estrutura

```
├── server.py          # MCP Server (stdio)
├── api.py             # REST API (FastAPI)
├── requirements.txt   # Dependências
├── .mcp.json         # Config Claude Code
├── .gitignore        # Segurança
├── render.yaml       # Config deploy Render
├── LICENSE           # MIT License
└── README.md         # Documentação
```

---

## Performance

| Métrica | Valor |
|---------|-------|
| **Fontes** | 10 (8 blogs + ArXiv + GitHub) |
| **Itens agregados** | ~180+ (2 semanas) |
| **Tempo primeira request** | 10-15s |
| **Tempo cache hit** | <100ms |
| **Cache TTL** | 15 minutos |
| **Timeout por request** | 30s |

**Otimizações:**
- Cache em memória
- Busca paralela de múltiplas fontes
- HTTP headers cache natural (ETags, Last-Modified)
- Timeout configurável

---

## Troubleshooting

### Claude não vê o servidor

- Verifique `.mcp.json` está na **raiz** do projeto
- Caminho correto no `args`
- Recarregue: `Ctrl+Shift+P` → "Reload Window"
- Teste: `python server.py` (não deve dar erro)

### API timeout (Render)

- Primeira request demora ~30s (cold start)
- Render free tier dorme após 15 min inatividade
- Requests seguintes são rápidas (cache)

### Erro de módulo

```bash
pip install -r requirements.txt --upgrade
```

### ArXiv/GitHub sem resultados

- Verifique conexão internet
- APIs podem ter rate limits temporários
- Tente aumentar `days` parameter (ex: `days=30`)

---

## Contribuindo

Contribuições são bem-vindas via Pull Requests!

**Guidelines:**
- Fork o repositório
- Crie branch: `git checkout -b feature/nova-feature`
- Commit: `git commit -m "Adiciona nova feature"`
- Push: `git push origin feature/nova-feature`
- Abra Pull Request

**Áreas para contribuir:**
- Adicionar novas fontes de dados
- Melhorar performance
- Adicionar testes unitários
- Melhorar documentação
- Tradução para inglês

---

## Autor

**Laura Mattos**

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue)](https://www.linkedin.com/in/lauramattosc/)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-black)](https://github.com/LauraMattz)

---

## Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## Créditos

- [Model Context Protocol (MCP)](https://modelcontextprotocol.io) - Framework MCP
- [FastAPI](https://fastapi.tiangolo.com) - Framework REST API
- [feedparser](https://feedparser.readthedocs.io/) - Parse RSS feeds
- [ArXiv API](https://arxiv.org/help/api) - Papers acadêmicos
- [GitHub API](https://docs.github.com/en/rest) - Repositórios trending

---

<div align="center">

**AI News Aggregator**

Mantendo a comunidade atualizada sobre Inteligência Artificial

[Live API](https://mcp-ai-news.onrender.com/docs) • [Docs](https://mcp-ai-news.onrender.com/redoc) • [Issues](https://github.com/LauraMattz/mcp_ai_news/issues)

Desenvolvido por [Laura Mattos](https://www.linkedin.com/in/lauramattosc/)

</div>
