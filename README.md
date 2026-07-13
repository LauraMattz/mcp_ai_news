# AI News Aggregator

Agregador de notícias de IA, papers acadêmicos e repositórios trending de 10 fontes confiáveis.

[![API Status](https://img.shields.io/website?url=https%3A%2F%2Fmcp-ai-news.onrender.com%2Fhealth&label=API)](https://mcp-ai-news.onrender.com/health)
[![Python](https://img.shields.io/badge/Python-3.10+-orange)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

---

## Quick Start

**Usar API (sem instalação):**
```bash
curl "https://mcp-ai-news.onrender.com/news?days=7&limit=5"
```

**Instalar MCP para Claude Code:**
```bash
git clone https://github.com/LauraMattz/mcp_ai_news.git && cd mcp_ai_news
pip install -r requirements.txt
# Recarregue Claude Code (Ctrl+Shift+P → Reload Window)
```

---

## API Pública

**Base:** `https://mcp-ai-news.onrender.com` | **Docs:** [Swagger UI](https://mcp-ai-news.onrender.com/docs)

| Endpoint | Descrição |
|----------|-----------|
| [/news?days=7&limit=10](https://mcp-ai-news.onrender.com/news?days=7&limit=10) | Todas as notícias |
| [/search?q=GPT](https://mcp-ai-news.onrender.com/search?q=GPT) | Busca por palavra-chave |
| [/papers?days=7](https://mcp-ai-news.onrender.com/papers?days=7) | Papers do ArXiv |
| [/github?days=7](https://mcp-ai-news.onrender.com/github?days=7) | Repos trending |

**Fontes:** OpenAI, Anthropic, Google AI, DeepMind, Hugging Face, MIT Tech Review, TechCrunch, The Verge, ArXiv (cs.AI/cs.LG/cs.CL/cs.CV/stat.ML), GitHub

**Features:** Cache 15 min • CORS habilitado • Gratuito • ~180+ itens agregados

---

## Instalação

### MCP Server (Claude Code)

O `.mcp.json` já está configurado na raiz do projeto. Após `git clone` e `pip install`, apenas recarregue Claude Code.

**Para Claude Desktop:**
Adicione ao `claude_desktop_config.json` ([Windows/Mac/Linux paths](https://modelcontextprotocol.io/quickstart)):
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

### REST API (Local)

```bash
python api.py
# Acesse: http://localhost:8000/docs
```

---

## Uso

**MCP (Claude Code/Desktop):**
```
"Liste as últimas notícias de IA"
"Busque conteúdo sobre transformers"
"Mostre papers do ArXiv sobre computer vision"
```

**API REST:**
```bash
curl "https://mcp-ai-news.onrender.com/news?days=7&limit=20"
curl "https://mcp-ai-news.onrender.com/search?q=GPT&days=14"
curl "https://mcp-ai-news.onrender.com/papers?days=3&max_results=10"
```

**Documentação completa:** [Swagger UI](https://mcp-ai-news.onrender.com/docs) • [ReDoc](https://mcp-ai-news.onrender.com/redoc)

---

## Desenvolvimento

**Adicionar fonte RSS:**
```python
# Em server.py e api.py
FONTES_RSS["nova_fonte"] = {
    "nome": "Nome", "url": "https://...", "ativa": True
}
```

**Testar:**
```bash
python server.py  # MCP Server
python api.py     # REST API → http://localhost:8000/docs
npx @modelcontextprotocol/inspector python server.py  # MCP Inspector
```

**Estrutura:**
```
├── server.py      # MCP Server (stdio)
├── api.py         # REST API (FastAPI)
├── .mcp.json      # Config Claude Code
└── render.yaml    # Deploy config
```

---

## Licença

MIT License - Ver [LICENSE](LICENSE)

**Desenvolvido por [Laura Mattos](https://github.com/LauraMattz)** • [LinkedIn](https://www.linkedin.com/in/lauramattosc/)

**Stack:** [MCP](https://modelcontextprotocol.io) • [FastAPI](https://fastapi.tiangolo.com) • [ArXiv API](https://arxiv.org/help/api)
