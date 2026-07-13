# AI News Aggregator

Agrega notícias, papers e repositórios sobre IA de múltiplas fontes confiáveis.

[![MCP](https://img.shields.io/badge/MCP-Enabled-blue)](https://modelcontextprotocol.io)
[![FastAPI](https://img.shields.io/badge/FastAPI-REST-green)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.10+-orange)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

---

## Features

- **10 fontes:** 8 blogs + ArXiv + GitHub
- **Filtro temporal:** Últimas 2 semanas (configurável)
- **Busca por palavra-chave**
- **MCP Server** para Claude Code/Desktop
- **REST API** para deploy remoto

**Fontes:** OpenAI, Anthropic, Google AI, DeepMind, Hugging Face, MIT Tech Review, TechCrunch, The Verge, ArXiv (cs.AI, cs.LG, cs.CL, cs.CV, stat.ML), GitHub Trending

---

## Instalação

### MCP Server (Claude Code/Desktop)

```bash
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Configurar .mcp.json na raiz do projeto
{
  "mcpServers": {
    "ai-news": {
      "command": "python",
      "args": ["server.py"]
    }
  }
}

# 3. Recarregar Claude Code: Ctrl+Shift+P → "Developer: Reload Window"
```

**Claude Desktop:** Edite `claude_desktop_config.json`:
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`
- Mac/Linux: `~/.config/Claude/claude_desktop_config.json`

---

## Uso

### MCP Tools (Claude Code/Desktop)

```
"Liste as últimas notícias de IA"
"Busque conteúdo sobre GPT"
"Mostre papers do ArXiv sobre transformers"
"Repositórios trending de ML"
```

**5 Tools disponíveis:**
- `list_ai_news` - Todas as fontes
- `search_ai_content` - Busca por keyword
- `list_arxiv_papers` - Papers acadêmicos
- `list_github_trending` - Repos populares
- `list_sources` - Fontes configuradas

---

## REST API

### Rodar localmente

```bash
python api.py
# Acesse: http://localhost:8000/docs
```

### Endpoints

| Endpoint | Descrição |
|----------|-----------|
| `GET /news` | Todas as notícias (blogs + papers + GitHub) |
| `GET /search?q=keyword` | Busca por palavra-chave |
| `GET /papers` | Papers do ArXiv |
| `GET /github` | Repos trending |
| `GET /sources` | Lista fontes |
| `GET /docs` | Documentação Swagger |

### Exemplos

```bash
curl http://localhost:8000/news?days=7&limit=20
curl http://localhost:8000/search?q=GPT&days=14
curl http://localhost:8000/papers?days=3&max_results=20
```

---

## Deploy (Render)

1. Criar conta: https://render.com
2. New Web Service → conectar repositório GitHub
3. Configuração automática via `render.yaml`
4. Deploy (~5 min)

**Build:** `pip install -r requirements.txt`
**Start:** `uvicorn api:app --host 0.0.0.0 --port $PORT`

---

## Estrutura

```
├── server.py          # MCP Server (stdio)
├── api.py             # REST API (FastAPI)
├── requirements.txt   # Dependências
├── .mcp.json         # Config Claude Code
├── render.yaml       # Deploy Render
└── README.md         # Documentação
```

---

## Desenvolvimento

### Adicionar fonte RSS

```python
# Em server.py e api.py
"nova_fonte": {
    "nome": "Nome da Fonte",
    "url": "https://fonte.com/rss.xml",
    "ativa": True
}
```

### Testar

```bash
# MCP Server
python server.py

# MCP Inspector
npx @modelcontextprotocol/inspector python server.py

# API REST
python api.py
```

---

## Performance

- ~180+ itens agregados em 10-15s
- Cache natural via HTTP headers
- Timeout: 30s por request
- Busca paralela de múltiplas fontes

---

## Troubleshooting

**Claude não vê o servidor:**
- Verifique `.mcp.json` está na raiz
- Recarregue: `Ctrl+Shift+P` → "Reload Window"

**API timeout:**
- Primeira request pode demorar ~30s (Render free tier)

**Erro de módulo:**
```bash
pip install -r requirements.txt
```

---

## License

MIT License - Ver [LICENSE](LICENSE)

---

## Autor

**[Laura Mattos](https://www.linkedin.com/in/lauramattosc/)**

---

## Créditos

- [MCP Framework](https://modelcontextprotocol.io)
- [FastAPI](https://fastapi.tiangolo.com)
- [ArXiv API](https://arxiv.org/help/api)
- [GitHub API](https://docs.github.com/en/rest)
