"""
FastAPI REST API - Agregador de Noticias de IA
API publica para buscar noticias, papers e repositorios sobre IA
"""

from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from typing import List, Dict, Optional
import feedparser
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
import xml.etree.ElementTree as ET
import requests
import time

# ============================================================================
# CACHE EM MEMORIA
# ============================================================================

CACHE = {}
CACHE_TTL = 900  # 15 minutos em segundos

def get_from_cache(key: str):
    """Busca item do cache se ainda válido"""
    if key in CACHE:
        data, timestamp = CACHE[key]
        if time.time() - timestamp < CACHE_TTL:
            print(f"[CACHE HIT] {key}")
            return data
        else:
            # Cache expirado, remover
            del CACHE[key]
    print(f"[CACHE MISS] {key}")
    return None

def save_to_cache(key: str, data):
    """Salva item no cache com timestamp"""
    CACHE[key] = (data, time.time())
    print(f"[CACHE SAVED] {key}")

# ============================================================================
# CONFIGURACAO FASTAPI
# ============================================================================

app = FastAPI(
    title="AI News Aggregator API",
    description="API para agregar notícias, papers e repositórios sobre Inteligência Artificial",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS - permitir acesso de qualquer origem
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# EXCEPTION HANDLERS
# ============================================================================

@app.exception_handler(405)
async def method_not_allowed_handler(request: Request, exc: StarletteHTTPException):
    """Handler para erros 405 - Method Not Allowed."""
    return JSONResponse(
        status_code=405,
        content={
            "error": "Method Not Allowed",
            "detail": f"O método {request.method} não é permitido para {request.url.path}",
            "allowed_methods": ["GET", "HEAD"] if request.url.path == "/health" else ["GET"],
            "hint": "Use GET para acessar este endpoint. Veja a documentação: /docs"
        }
    )

# ============================================================================
# CONFIGURACAO DE FONTES
# ============================================================================

FONTES_RSS = {
    "openai": {
        "nome": "OpenAI Blog",
        "url": "https://openai.com/news/rss.xml",
        "ativa": True
    },
    "anthropic": {
        "nome": "Anthropic News",
        "url": "https://www.anthropic.com/news/rss.xml",
        "ativa": True
    },
    "google_ai": {
        "nome": "Google AI Blog",
        "url": "https://blog.google/technology/ai/rss/",
        "ativa": True
    },
    "deepmind": {
        "nome": "DeepMind Blog",
        "url": "https://deepmind.google/blog/rss.xml",
        "ativa": True
    },
    "huggingface": {
        "nome": "Hugging Face Blog",
        "url": "https://huggingface.co/blog/feed.xml",
        "ativa": True
    },
    "mit_tech": {
        "nome": "MIT Technology Review - AI",
        "url": "https://www.technologyreview.com/topic/artificial-intelligence/feed",
        "ativa": True
    },
    "techcrunch_ai": {
        "nome": "TechCrunch AI",
        "url": "https://techcrunch.com/tag/artificial-intelligence/feed/",
        "ativa": True
    },
    "theverge_ai": {
        "nome": "The Verge AI",
        "url": "https://www.theverge.com/ai-artificial-intelligence/rss/index.xml",
        "ativa": True
    }
}

ARXIV_CATEGORIAS = ["cs.AI", "cs.LG", "cs.CL", "cs.CV", "stat.ML"]

# ============================================================================
# FUNCOES DE BUSCA (reutilizadas do server.py)
# ============================================================================

def buscar_arxiv_papers(dias: int = 14, max_results: int = 50) -> List[Dict]:
    """Busca papers recentes do ArXiv em categorias de IA/ML."""
    try:
        data_corte = datetime.now(timezone.utc) - timedelta(days=dias)
        categorias_query = " OR ".join([f"cat:{cat}" for cat in ARXIV_CATEGORIAS])
        query = f"({categorias_query})"

        base_url = "http://export.arxiv.org/api/query"
        params = {
            "search_query": query,
            "start": 0,
            "max_results": max_results,
            "sortBy": "submittedDate",
            "sortOrder": "descending"
        }

        response = requests.get(base_url, params=params, timeout=30)
        response.raise_for_status()

        root = ET.fromstring(response.content)
        ns = {'atom': 'http://www.w3.org/2005/Atom', 'arxiv': 'http://arxiv.org/schemas/atom'}

        papers = []
        for entry in root.findall('atom:entry', ns):
            try:
                published_str = entry.find('atom:published', ns).text
                published_date = datetime.fromisoformat(published_str.replace('Z', '+00:00'))

                if published_date >= data_corte:
                    title = entry.find('atom:title', ns).text.strip().replace('\n', ' ')
                    summary = entry.find('atom:summary', ns).text.strip().replace('\n', ' ')
                    link_elem = entry.find('atom:id', ns)
                    link = link_elem.text if link_elem is not None else ""

                    authors = []
                    for author in entry.findall('atom:author', ns):
                        name_elem = author.find('atom:name', ns)
                        if name_elem is not None:
                            authors.append(name_elem.text)

                    categories = []
                    for cat in entry.findall('atom:category', ns):
                        term = cat.get('term')
                        if term:
                            categories.append(term)

                    paper = {
                        "fonte": "ArXiv",
                        "titulo": title,
                        "link": link,
                        "data": published_str,
                        "resumo": summary[:300] + "..." if len(summary) > 300 else summary,
                        "autores": authors[:3],
                        "categorias": categories
                    }
                    papers.append(paper)
            except Exception:
                continue

        return papers

    except Exception as e:
        print(f"[ArXiv] ERRO: {e}")
        return []


def buscar_github_trending(dias: int = 14, max_results: int = 30) -> List[Dict]:
    """Busca repositorios populares de IA no GitHub."""
    try:
        data_corte = datetime.now(timezone.utc) - timedelta(days=dias)
        data_str = data_corte.strftime("%Y-%m-%d")
        query = f"topic:artificial-intelligence pushed:>{data_str} stars:>10"

        url = "https://api.github.com/search/repositories"
        params = {
            "q": query,
            "sort": "stars",
            "order": "desc",
            "per_page": max_results
        }

        headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "AI-News-Aggregator-API"
        }

        response = requests.get(url, params=params, headers=headers, timeout=30)
        response.raise_for_status()

        data = response.json()
        repos = []

        for item in data.get("items", []):
            try:
                created_date = datetime.fromisoformat(item["created_at"].replace('Z', '+00:00'))
                updated_date = datetime.fromisoformat(item["updated_at"].replace('Z', '+00:00'))
                data_relevante = max(created_date, updated_date)

                repo = {
                    "fonte": "GitHub",
                    "titulo": f"{item['full_name']} - {item['description'] or 'Sem descricao'}",
                    "link": item["html_url"],
                    "data": item["updated_at"],
                    "resumo": item.get("description", "Sem descricao"),
                    "stars": item.get("stargazers_count", 0),
                    "linguagem": item.get("language", "N/A"),
                    "topics": item.get("topics", [])[:5]
                }
                repos.append(repo)
            except Exception:
                continue

        return repos

    except Exception as e:
        print(f"[GitHub] ERRO: {e}")
        return []


def buscar_noticias_rss(feed_url: str, fonte_nome: str, dias: int = 14) -> List[Dict]:
    """Busca noticias de qualquer feed RSS."""
    try:
        feed = feedparser.parse(feed_url)
        data_corte = datetime.now(timezone.utc) - timedelta(days=dias)

        noticias = []
        for entry in feed.entries:
            try:
                data_str = None
                if hasattr(entry, 'published'):
                    data_str = entry.published
                elif hasattr(entry, 'updated'):
                    data_str = entry.updated

                if data_str:
                    data_publicacao = parsedate_to_datetime(data_str)

                    if data_publicacao >= data_corte:
                        resumo = ""
                        if hasattr(entry, 'summary'):
                            resumo = entry.summary
                        elif hasattr(entry, 'description'):
                            resumo = entry.description

                        noticia = {
                            "fonte": fonte_nome,
                            "titulo": entry.title,
                            "link": entry.link,
                            "data": data_str,
                            "resumo": resumo
                        }
                        noticias.append(noticia)
            except Exception:
                continue

        return noticias

    except Exception as e:
        print(f"[{fonte_nome}] ERRO: {e}")
        return []


def buscar_todas_fontes(dias: int = 14, incluir_papers: bool = True, incluir_github: bool = True) -> List[Dict]:
    """Busca de TODAS as fontes: RSS, ArXiv e GitHub."""
    todas_noticias = []

    # RSS feeds
    for fonte_id, config in FONTES_RSS.items():
        if config['ativa']:
            noticias = buscar_noticias_rss(config['url'], config['nome'], dias)
            todas_noticias.extend(noticias)

    # ArXiv papers
    if incluir_papers:
        papers = buscar_arxiv_papers(dias=dias, max_results=50)
        todas_noticias.extend(papers)

    # GitHub trending
    if incluir_github:
        repos = buscar_github_trending(dias=dias, max_results=30)
        todas_noticias.extend(repos)

    # Ordena por data (mais recente primeiro)
    todas_noticias.sort(key=lambda x: x.get('data', ''), reverse=True)

    return todas_noticias


# ============================================================================
# ENDPOINTS REST API
# ============================================================================

@app.get("/")
async def root():
    """Endpoint raiz com informacoes da API."""
    return {
        "nome": "AI News Aggregator API",
        "versao": "1.0.0",
        "descricao": "API para agregar noticias, papers e repositorios sobre IA",
        "endpoints": {
            "GET /news": "Lista todas as noticias agregadas",
            "GET /search": "Busca por palavra-chave",
            "GET /papers": "Lista apenas papers do ArXiv",
            "GET /github": "Lista apenas repos do GitHub",
            "GET /sources": "Lista fontes configuradas",
            "GET /docs": "Documentacao interativa (Swagger)",
            "GET /health": "Status da API"
        },
        "fontes": f"{len(FONTES_RSS)} blogs + ArXiv + GitHub",
        "repositorio": "https://github.com/yourusername/ai-news-aggregator"
    }


@app.get("/health")
@app.head("/health")
async def health():
    """Health check endpoint (GET e HEAD)."""
    return {
        "status": "ok",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


@app.get("/news")
async def get_news(
    days: int = Query(14, ge=1, le=90, description="Numero de dias retroativos (1-90)"),
    include_papers: bool = Query(True, description="Incluir papers do ArXiv"),
    include_github: bool = Query(True, description="Incluir repos do GitHub"),
    limit: Optional[int] = Query(None, ge=1, le=200, description="Limitar resultados")
):
    """
    Lista todas as noticias, papers e repositorios agregados.

    **Parametros:**
    - **days**: Numero de dias retroativos (default: 14)
    - **include_papers**: Incluir papers do ArXiv (default: true)
    - **include_github**: Incluir repos do GitHub (default: true)
    - **limit**: Limitar numero de resultados (opcional)
    """
    try:
        # Chave de cache unica
        cache_key = f"news_{days}_{include_papers}_{include_github}_{limit}"

        # Tentar pegar do cache
        cached = get_from_cache(cache_key)
        if cached:
            return cached

        # Se não tem cache, buscar
        noticias = buscar_todas_fontes(
            dias=days,
            incluir_papers=include_papers,
            incluir_github=include_github
        )

        if limit:
            noticias = noticias[:limit]

        # Agrupa por fonte para estatisticas
        fontes_count = {}
        for n in noticias:
            fonte = n.get('fonte', 'Desconhecido')
            fontes_count[fonte] = fontes_count.get(fonte, 0) + 1

        result = {
            "total": len(noticias),
            "dias": days,
            "fontes": fontes_count,
            "resultados": noticias
        }

        # Salvar no cache
        save_to_cache(cache_key, result)

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar noticias: {str(e)}")


@app.get("/search")
async def search_content(
    q: str = Query(..., min_length=2, description="Palavra-chave para busca"),
    days: int = Query(14, ge=1, le=90, description="Numero de dias retroativos")
):
    """
    Busca por palavra-chave em titulos e resumos.

    **Parametros:**
    - **q**: Palavra-chave (obrigatorio, min 2 caracteres)
    - **days**: Numero de dias retroativos (default: 14)
    """
    try:
        cache_key = f"search_{q.lower()}_{days}"

        # Tentar cache
        cached = get_from_cache(cache_key)
        if cached:
            return cached

        todas = buscar_todas_fontes(dias=days)
        keyword_lower = q.lower()

        filtradas = [
            n for n in todas
            if keyword_lower in n['titulo'].lower() or keyword_lower in n.get('resumo', '').lower()
        ]

        result = {
            "keyword": q,
            "total": len(filtradas),
            "dias": days,
            "resultados": filtradas
        }

        save_to_cache(cache_key, result)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na busca: {str(e)}")


@app.get("/papers")
async def get_papers(
    days: int = Query(14, ge=1, le=90, description="Numero de dias retroativos"),
    max_results: int = Query(50, ge=1, le=100, description="Maximo de papers")
):
    """
    Lista apenas papers academicos do ArXiv.

    **Parametros:**
    - **days**: Numero de dias retroativos (default: 14)
    - **max_results**: Maximo de papers (default: 50, max: 100)
    """
    try:
        cache_key = f"papers_{days}_{max_results}"

        cached = get_from_cache(cache_key)
        if cached:
            return cached

        papers = buscar_arxiv_papers(dias=days, max_results=max_results)

        result = {
            "total": len(papers),
            "dias": days,
            "categorias": ARXIV_CATEGORIAS,
            "resultados": papers
        }

        save_to_cache(cache_key, result)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar papers: {str(e)}")


@app.get("/github")
async def get_github_trending(
    days: int = Query(14, ge=1, le=90, description="Numero de dias retroativos"),
    max_results: int = Query(30, ge=1, le=50, description="Maximo de repositorios")
):
    """
    Lista repositorios trending de IA no GitHub.

    **Parametros:**
    - **days**: Numero de dias retroativos (default: 14)
    - **max_results**: Maximo de repos (default: 30, max: 50)
    """
    try:
        cache_key = f"github_{days}_{max_results}"

        cached = get_from_cache(cache_key)
        if cached:
            return cached

        repos = buscar_github_trending(dias=days, max_results=max_results)

        result = {
            "total": len(repos),
            "dias": days,
            "resultados": repos
        }

        save_to_cache(cache_key, result)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar GitHub: {str(e)}")


@app.get("/sources")
async def get_sources():
    """
    Lista todas as fontes de conteudo configuradas.

    Retorna status de blogs RSS, ArXiv e GitHub.
    """
    blogs = []
    for fonte_id, config in FONTES_RSS.items():
        blogs.append({
            "id": fonte_id,
            "nome": config['nome'],
            "url": config['url'],
            "ativa": config['ativa']
        })

    return {
        "total_fontes": len(blogs) + 2,  # +2 para ArXiv e GitHub
        "blogs_rss": {
            "total": len(blogs),
            "fontes": blogs
        },
        "arxiv": {
            "categorias": ARXIV_CATEGORIAS,
            "url": "http://export.arxiv.org/api/query"
        },
        "github": {
            "api": "https://api.github.com/search/repositories",
            "topics": ["artificial-intelligence", "machine-learning", "deep-learning"]
        }
    }


# ============================================================================
# INICIALIZACAO
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    print("=== AI News Aggregator API ===")
    print("Iniciando servidor na porta 8000...")
    print("Documentacao: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)
