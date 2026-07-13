# Estrutura do Repositório

Este documento descreve a organização dos arquivos no projeto.

```
ai-news-aggregator/
│
├── server.py              # Servidor MCP para uso local (Claude Code/Desktop)
├── api.py                 # API REST FastAPI para deploy em servidor
│
├── requirements.txt       # Dependências Python (MCP + FastAPI)
│
├── .mcp.json             # Configuração MCP para Claude Code
├── .gitignore            # Arquivos a ignorar (segurança)
│
├── README.md             # Documentação principal do projeto
├── DEPLOY.md             # Guia completo de deploy
├── STRUCTURE.md          # Este arquivo (estrutura do repo)
├── LICENSE               # Licença MIT
│
├── Procfile              # Config para Render/Heroku
├── render.yaml           # Config específica do Render
├── railway.json          # Config específica do Railway
├── Dockerfile            # Container Docker (deploy universal)
└── runtime.txt           # Versão Python para plataformas
```

---

## Descrição dos Arquivos

### Arquivos Principais

**`server.py`** (604 linhas, 21KB)
- Servidor MCP usando protocolo stdio
- Para uso LOCAL com Claude Code ou Claude Desktop
- 10 fontes de conteúdo: 8 blogs + ArXiv + GitHub
- 5 tools MCP: list_ai_news, search_ai_content, list_arxiv_papers, list_github_trending, list_sources

**`api.py`** (500+ linhas, 16KB)
- API REST usando FastAPI
- Para DEPLOY em servidor remoto (Render/Railway/Fly.io)
- Mesma lógica de busca do server.py, mas com endpoints HTTP
- Documentação automática (Swagger/ReDoc)
- CORS habilitado para acesso público

---

### Arquivos de Configuração

**`.mcp.json`**
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
- Configuração do MCP para Claude Code
- DEVE estar na raiz do projeto (não em `.claude/`)

**`requirements.txt`**
```
mcp>=1.0.0              # Framework MCP
fastapi>=0.109.0        # API REST
uvicorn[standard]       # Servidor ASGI
feedparser>=6.0.10      # Parse RSS
requests>=2.31.0        # HTTP requests
aiohttp>=3.9.0          # Async HTTP
```

**`.gitignore`**
- Protege dados sensíveis (.env, credentials, API keys)
- Ignora cache (__pycache__, *.pyc)
- Ignora logs e arquivos temporários
- Ignora configurações locais

---

### Arquivos de Deploy

**`Procfile`** (Render/Heroku)
```
web: uvicorn api:app --host 0.0.0.0 --port $PORT
```

**`render.yaml`** (Render.com)
- Define serviço web Python
- Build command: pip install
- Start command: uvicorn

**`railway.json`** (Railway.app)
- Config para Nixpacks builder
- Start command e restart policy

**`Dockerfile`** (Deploy universal)
- Imagem Python 3.10-slim
- Copia apenas api.py e requirements
- Expõe porta 8000

**`runtime.txt`**
```
python-3.10.0
```
- Define versão Python para plataformas

---

### Documentação

**`README.md`**
- Visão geral do projeto
- Features e arquitetura
- Instalação e uso (MCP local)
- API reference
- Troubleshooting

**`DEPLOY.md`**
- Guia completo de deploy
- 4 opções: Render, Railway, Fly.io, Docker
- Instruções passo-a-passo
- Testes e monitoramento
- Custos estimados

**`STRUCTURE.md`** (este arquivo)
- Organização do repositório
- Descrição de cada arquivo
- Fluxo de trabalho

**`LICENSE`**
- MIT License (open-source)

---

## Fluxo de Trabalho

### Desenvolvimento Local

1. **Instalar dependências:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Testar MCP Server:**
   ```bash
   python server.py
   # Ou usar Claude Code com .mcp.json configurado
   ```

3. **Testar API REST:**
   ```bash
   python api.py
   # ou: uvicorn api:app --reload
   # Acesse: http://localhost:8000/docs
   ```

### Deploy em Produção

1. **Push para GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Deploy:**
   - **Render:** Conecta GitHub, usa `render.yaml`
   - **Railway:** Conecta GitHub, usa `railway.json`
   - **Fly.io:** `fly launch && fly deploy`
   - **Docker:** `docker build -t ai-news-api .`

3. **Usar API:**
   ```bash
   curl https://SEU_APP.onrender.com/news?days=7
   ```

---

## Segurança

### Arquivos Protegidos (.gitignore)

- **.env**: Variáveis de ambiente (API keys futuras)
- **credentials.json**: Credenciais de serviços
- **config.local.py**: Configurações locais
- **__pycache__/**: Cache Python
- **logs/**: Arquivos de log
- **.vscode/**, **.idea/**: Configurações de IDE

### Boas Práticas

- Nunca commit API keys ou tokens
- Use variáveis de ambiente para segredos
- Mantenha logs fora do repositório
- Revise .gitignore antes de cada commit

---

## Dependências

### Produção

| Pacote | Versão | Uso |
|--------|--------|-----|
| mcp | >=1.0.0 | Framework MCP (local) |
| fastapi | >=0.109.0 | Framework API REST |
| uvicorn | >=0.27.0 | Servidor ASGI |
| feedparser | >=6.0.10 | Parse RSS feeds |
| requests | >=2.31.0 | HTTP requests (ArXiv/GitHub) |
| aiohttp | >=3.9.0 | Async HTTP (futuro) |

### Desenvolvimento (opcional)

```bash
pip install pytest black flake8 mypy
```

---

## Manutenção

### Adicionar Nova Fonte RSS

Edite `FONTES_RSS` em `server.py` e `api.py`:

```python
"nova_fonte": {
    "nome": "Nome da Fonte",
    "url": "https://fonte.com/rss.xml",
    "ativa": True
}
```

### Adicionar Nova Categoria ArXiv

Edite `ARXIV_CATEGORIAS`:

```python
ARXIV_CATEGORIAS = ["cs.AI", "cs.LG", "cs.CL", "cs.CV", "stat.ML", "cs.RO"]
```

### Atualizar Dependências

```bash
pip list --outdated
pip install --upgrade fastapi uvicorn requests
pip freeze > requirements.txt
```

---

## Tamanho dos Arquivos

```
Total: ~50KB (código) + ~15KB (docs) + ~1KB (config)

server.py:        21KB  (MCP)
api.py:           16KB  (REST)
README.md:        10KB
DEPLOY.md:         9KB
STRUCTURE.md:      6KB (este arquivo)
requirements.txt:  334B
.mcp.json:         104B
.gitignore:       1.5KB
```

---

## Links Úteis

- **MCP Docs:** https://modelcontextprotocol.io
- **FastAPI Docs:** https://fastapi.tiangolo.com
- **ArXiv API:** https://arxiv.org/help/api
- **GitHub API:** https://docs.github.com/en/rest
- **Render Docs:** https://render.com/docs
- **Railway Docs:** https://docs.railway.app

---

**Última atualização:** 2026-07-13
