# Guia de Deploy - AI News Aggregator API

Este guia mostra como fazer deploy da API REST em serviços de hosting gratuitos.

---

## Arquitetura

```
Local (MCP):
Claude Code/Desktop → server.py (MCP stdio)

Cloud (API REST):
Internet → api.py (FastAPI HTTP) → Render/Railway/Fly.io
```

---

## Opção 1: Render (Recomendado)

**Grátis:** 750 horas/mês, SSL automático, fácil configuração

### Passo-a-passo:

1. **Criar conta no Render**
   - Acesse: https://render.com
   - Sign up com GitHub (recomendado)

2. **Fazer push do código para GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit - AI News Aggregator API"
   git branch -M main
   git remote add origin https://github.com/SEU_USUARIO/ai-news-aggregator.git
   git push -u origin main
   ```

3. **Criar novo Web Service no Render**
   - Dashboard → "New" → "Web Service"
   - Conecte seu repositório GitHub
   - Configure:
     - **Name:** `ai-news-aggregator`
     - **Region:** Oregon (US West) ou próximo
     - **Branch:** `main`
     - **Runtime:** Python 3
     - **Build Command:** `pip install -r requirements.txt`
     - **Start Command:** `uvicorn api:app --host 0.0.0.0 --port $PORT`
     - **Plan:** Free

4. **Deploy automático**
   - Render detecta `render.yaml` e faz deploy
   - Aguarde 5-10 minutos
   - Acesse: `https://ai-news-aggregator-XXXXX.onrender.com`

5. **Testar API**
   ```bash
   curl https://SEU_APP.onrender.com/health
   curl https://SEU_APP.onrender.com/news?days=7
   ```

### Limitações do Plano Grátis:
- ⏰ 750 horas/mês (suficiente para uso moderado)
- 🐌 Pode "dormir" após 15 min de inatividade (primeira request demora ~30s)
- 📊 512 MB RAM, CPU compartilhado

---

## Opção 2: Railway

**Grátis:** 500 horas/mês, $5 crédito inicial, deploy rápido

### Passo-a-passo:

1. **Criar conta no Railway**
   - Acesse: https://railway.app
   - Login com GitHub

2. **Push para GitHub** (mesmo processo da Opção 1)

3. **Criar novo projeto**
   - Dashboard → "New Project"
   - "Deploy from GitHub repo"
   - Selecione seu repositório
   - Railway detecta Python automaticamente

4. **Configurar variáveis (opcional)**
   - Settings → Variables
   - Adicione se necessário (ex: API keys futuras)

5. **Deploy automático**
   - Railway usa `railway.json` automaticamente
   - Domain público gerado: `https://XXXXX.up.railway.app`

6. **Testar**
   ```bash
   curl https://SEU_APP.up.railway.app/docs
   ```

### Limitações:
- ⏰ 500h/mês ou $5 crédito (o que acabar primeiro)
- 💳 Requer cartão após trial (mas não cobra se não passar do free tier)

---

## Opção 3: Fly.io

**Grátis:** $5 crédito mensal, bom uptime, sem sleep

### Passo-a-passo:

1. **Instalar Fly CLI**
   ```bash
   # Windows (PowerShell)
   iwr https://fly.io/install.ps1 -useb | iex

   # Mac/Linux
   curl -L https://fly.io/install.sh | sh
   ```

2. **Login**
   ```bash
   fly auth login
   ```

3. **Inicializar app**
   ```bash
   cd /caminho/para/seu/repo
   fly launch
   ```
   - Nome: `ai-news-aggregator`
   - Region: escolha a mais próxima
   - PostgreSQL: **No** (não precisa)
   - Redis: **No**

4. **Deploy**
   ```bash
   fly deploy
   ```

5. **Verificar**
   ```bash
   fly status
   fly open
   ```

### Vantagens:
- ✅ Sem cold start (não dorme)
- ✅ $5/mês é suficiente para uso moderado
- ✅ Melhor uptime

### Limitações:
- 💳 Requer cartão de crédito (mas não cobra se usar só $5)

---

## Opção 4: Docker (Qualquer Host)

Use o `Dockerfile` incluído para deploy em qualquer plataforma que suporte containers.

### Testar localmente:

```bash
# Build
docker build -t ai-news-api .

# Run
docker run -p 8000:8000 ai-news-api

# Testar
curl http://localhost:8000/health
```

### Deploy em plataformas:
- **Google Cloud Run** (2M requests/mês grátis)
- **AWS App Runner**
- **Azure Container Instances**
- **DigitalOcean App Platform** ($5/mês)

---

## Teste Local Antes de Deploy

Sempre teste localmente antes de fazer deploy:

```bash
# Instalar dependências
pip install -r requirements.txt

# Rodar API
python api.py

# Ou com uvicorn
uvicorn api:app --reload

# Testar endpoints
curl http://localhost:8000/
curl http://localhost:8000/health
curl http://localhost:8000/news?days=7&limit=10
curl http://localhost:8000/search?q=GPT&days=14
curl http://localhost:8000/papers?days=7
curl http://localhost:8000/github?days=7
curl http://localhost:8000/sources
```

Acesse documentação interativa:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## Endpoints da API

| Endpoint | Método | Descrição |
|----------|--------|-----------|
| `/` | GET | Info da API |
| `/health` | GET | Health check |
| `/news` | GET | Todas as notícias (blogs + papers + GitHub) |
| `/search?q=keyword` | GET | Busca por palavra-chave |
| `/papers` | GET | Apenas papers do ArXiv |
| `/github` | GET | Apenas repos do GitHub |
| `/sources` | GET | Lista todas as fontes |
| `/docs` | GET | Documentação Swagger |

### Exemplos de uso:

```bash
# Últimas notícias (14 dias)
GET /news

# Notícias dos últimos 7 dias, limite 20
GET /news?days=7&limit=20

# Apenas notícias de blogs (sem papers/github)
GET /news?include_papers=false&include_github=false

# Buscar por "transformer"
GET /search?q=transformer&days=14

# Papers dos últimos 3 dias
GET /papers?days=3&max_results=20

# Trending repos da última semana
GET /github?days=7&max_results=15
```

---

## Como Usar a API no Claude

Depois de fazer deploy, você pode usar a API com Claude de 3 formas:

### 1. Custom Actions (Claude Web)

Configure um Custom Action no Claude Web com a URL da sua API:

```yaml
openapi: 3.0.0
info:
  title: AI News Aggregator
  version: 1.0.0
servers:
  - url: https://SEU_APP.onrender.com
paths:
  /news:
    get:
      operationId: getNews
      parameters:
        - name: days
          in: query
          schema:
            type: integer
            default: 14
```

### 2. Function Calling (Claude API)

Use via API do Claude com function calling:

```python
import anthropic

client = anthropic.Anthropic(api_key="sua-api-key")

tools = [
    {
        "name": "get_ai_news",
        "description": "Busca notícias recentes sobre IA",
        "input_schema": {
            "type": "object",
            "properties": {
                "days": {"type": "integer", "description": "Dias retroativos"}
            }
        }
    }
]
```

### 3. Simplesmente forneça a URL

Cole a URL da API em qualquer conversa com Claude:

```
Claude, acesse https://SEU_APP.onrender.com/news?days=7
e me dê um resumo das principais notícias de IA da última semana.
```

---

## Monitoramento

### Render:
- Dashboard → Seu serviço → "Logs" (logs em tempo real)
- "Metrics" (uso de CPU/RAM)

### Railway:
- Dashboard → Projeto → "Deployments"
- Ver logs de cada deploy

### Fly.io:
```bash
fly logs
fly status
fly dashboard
```

---

## Custos Estimados

| Plataforma | Free Tier | Custo após free tier |
|------------|-----------|---------------------|
| **Render** | 750h/mês | $7/mês (starter) |
| **Railway** | 500h ou $5 | $5/mês + uso |
| **Fly.io** | $5 crédito/mês | $0.0000022/s (~$5.70/mês) |
| **Vercel** | Hobby free | $20/mês (pro) |

**Recomendação:** Render para começar (mais simples), Fly.io para produção (melhor uptime).

---

## Troubleshooting

### Erro: "Port already in use"
```bash
# Matar processo na porta 8000
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:8000 | xargs kill -9
```

### Erro: "Module not found"
```bash
pip install -r requirements.txt --upgrade
```

### API retorna 502/503
- Aguarde cold start (~30s em Render free tier)
- Verifique logs no dashboard
- Confirme que `PORT` env var está configurada

### ArXiv/GitHub timeout
- Normal em primeira request (cache cold)
- APIs externas podem ter rate limits
- Adicione tratamento de timeout se necessário

---

## Próximos Passos

Depois do deploy:

1. **Adicionar cache Redis** (melhorar performance)
2. **Rate limiting** (evitar abuso)
3. **API Key auth** (se quiser tornar privada)
4. **Webhook notifications** (alertas para novas notícias)
5. **Dashboard frontend** (visualização web)

---

## Suporte

- **Render Docs:** https://render.com/docs
- **Railway Docs:** https://docs.railway.app
- **Fly.io Docs:** https://fly.io/docs
- **FastAPI Docs:** https://fastapi.tiangolo.com

Para issues com este projeto, abra uma issue no GitHub.

---

**Bom deploy!** 🚀
