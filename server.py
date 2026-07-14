"""
MCP Server - Agregador de Noticias de IA
Busca noticias, papers e repositorios sobre Inteligencia Artificial
"""

from mcp.server import Server
from mcp.types import Tool, TextContent
import mcp.server.stdio
import feedparser
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
import asyncio
import aiohttp
from typing import List, Dict
import urllib.parse
import xml.etree.ElementTree as ET

app = Server("ai-news-aggregator")

print("=== AI News Aggregator MCP Server ===")
print("Inicializando...")

# ============================================================================
# CONFIGURACAO DE FONTES RSS
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
    },
    "meta_research": {
        "nome": "Meta Research",
        "url": "https://research.facebook.com/feed/",
        "ativa": True
    },
    "nvidia_blog": {
        "nome": "Nvidia Blog",
        "url": "https://blogs.nvidia.com/feed/",
        "ativa": True
    },
    "stanford_hai": {
        "nome": "Stanford HAI",
        "url": "https://hai.stanford.edu/news/rss.xml",
        "ativa": True
    },
    "mit_csail": {
        "nome": "MIT CSAIL",
        "url": "https://news.mit.edu/rss/topic/computer-science-and-artificial-intelligence-laboratory-csail",
        "ativa": True
    }
}

# ============================================================================
# CONFIGURACAO ARXIV
# ============================================================================

ARXIV_CATEGORIAS = ["cs.AI", "cs.LG", "cs.CL", "cs.CV", "stat.ML"]

# ============================================================================
# FUNCAO: Buscar papers do ArXiv
# ============================================================================

def buscar_arxiv_papers(dias: int = 14, max_results: int = 50) -> List[Dict]:
    """
    Busca papers recentes do ArXiv em categorias de IA/ML.

    Args:
        dias: Numero de dias para buscar
        max_results: Maximo de papers por categoria

    Returns:
        Lista de papers formatados
    """
    try:
        import requests

        data_corte = datetime.now(timezone.utc) - timedelta(days=dias)

        # Query para buscar papers em categorias de IA
        categorias_query = " OR ".join([f"cat:{cat}" for cat in ARXIV_CATEGORIAS])
        query = f"({categorias_query})"

        # API do ArXiv
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

        # Parse XML
        root = ET.fromstring(response.content)
        ns = {'atom': 'http://www.w3.org/2005/Atom', 'arxiv': 'http://arxiv.org/schemas/atom'}

        papers = []
        for entry in root.findall('atom:entry', ns):
            try:
                # Data de publicacao
                published_str = entry.find('atom:published', ns).text
                published_date = datetime.fromisoformat(published_str.replace('Z', '+00:00'))

                if published_date >= data_corte:
                    # Extrai informacoes
                    title = entry.find('atom:title', ns).text.strip().replace('\n', ' ')
                    summary = entry.find('atom:summary', ns).text.strip().replace('\n', ' ')

                    # Link
                    link_elem = entry.find('atom:id', ns)
                    link = link_elem.text if link_elem is not None else ""

                    # Autores
                    authors = []
                    for author in entry.findall('atom:author', ns):
                        name_elem = author.find('atom:name', ns)
                        if name_elem is not None:
                            authors.append(name_elem.text)

                    # Categorias
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
                        "data_obj": published_date,
                        "resumo": summary[:300] + "..." if len(summary) > 300 else summary,
                        "autores": authors[:3],  # Primeiros 3 autores
                        "categorias": categories
                    }
                    papers.append(paper)
            except Exception as e:
                continue

        print(f"[ArXiv] {len(papers)} papers encontrados")
        return papers

    except Exception as e:
        print(f"[ArXiv] ERRO: {e}")
        return []


# ============================================================================
# FUNCAO: Buscar GitHub Trending
# ============================================================================

def buscar_github_trending(dias: int = 14, max_results: int = 30) -> List[Dict]:
    """
    Busca repositorios populares de IA no GitHub.

    Args:
        dias: Numero de dias para buscar
        max_results: Maximo de repositorios

    Returns:
        Lista de repositorios formatados
    """
    try:
        import requests

        data_corte = datetime.now(timezone.utc) - timedelta(days=dias)
        data_str = data_corte.strftime("%Y-%m-%d")

        # Query simplificada: repos com topic AI e muitas stars
        # Busca repos com topic "artificial-intelligence" criados/atualizados recentemente
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
            "User-Agent": "AI-News-Aggregator-MCP"
        }

        response = requests.get(url, params=params, headers=headers, timeout=30)
        response.raise_for_status()

        data = response.json()
        repos = []

        for item in data.get("items", []):
            try:
                created_date = datetime.fromisoformat(item["created_at"].replace('Z', '+00:00'))
                updated_date = datetime.fromisoformat(item["updated_at"].replace('Z', '+00:00'))

                # Usa a data mais recente
                data_relevante = max(created_date, updated_date)

                repo = {
                    "fonte": "GitHub",
                    "titulo": f"{item['full_name']} - {item['description'] or 'Sem descricao'}",
                    "link": item["html_url"],
                    "data": item["updated_at"],
                    "data_obj": data_relevante,
                    "resumo": item.get("description", "Sem descricao"),
                    "stars": item.get("stargazers_count", 0),
                    "linguagem": item.get("language", "N/A"),
                    "topics": item.get("topics", [])[:5]
                }
                repos.append(repo)
            except Exception as e:
                continue

        print(f"[GitHub] {len(repos)} repositorios encontrados")
        return repos

    except Exception as e:
        print(f"[GitHub] ERRO: {e}")
        return []


# ============================================================================
# FUNCAO GENERICA: Buscar noticias de RSS
# ============================================================================

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
                            "data_obj": data_publicacao,
                            "resumo": resumo
                        }
                        noticias.append(noticia)
            except Exception as e:
                continue

        print(f"[{fonte_nome}] {len(noticias)} noticias encontradas")
        return noticias

    except Exception as e:
        print(f"[{fonte_nome}] ERRO ao buscar: {e}")
        return []


# ============================================================================
# FUNCAO: Buscar de todas as fontes
# ============================================================================

def buscar_todas_fontes(dias: int = 14, incluir_papers: bool = True, incluir_github: bool = True) -> List[Dict]:
    """
    Busca de TODAS as fontes: RSS, ArXiv e GitHub.

    Args:
        dias: Numero de dias
        incluir_papers: Se deve incluir papers do ArXiv
        incluir_github: Se deve incluir repos do GitHub

    Returns:
        Lista combinada e ordenada
    """
    total_fontes = len([f for f in FONTES_RSS.values() if f['ativa']])
    if incluir_papers:
        total_fontes += 1
    if incluir_github:
        total_fontes += 1

    print(f"\nBuscando das ultimas {dias} dias de {total_fontes} fontes...")
    print("-" * 70)

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

    # Ordena por data
    todas_noticias.sort(key=lambda x: x['data_obj'], reverse=True)

    print("-" * 70)
    print(f"TOTAL: {len(todas_noticias)} itens de {total_fontes} fontes\n")

    return todas_noticias


# ============================================================================
# FUNCAO: Buscar por palavra-chave
# ============================================================================

def buscar_por_keyword(keyword: str, dias: int = 14) -> List[Dict]:
    """Busca itens que contenham uma palavra-chave."""
    todas = buscar_todas_fontes(dias)
    keyword_lower = keyword.lower()

    filtradas = [
        n for n in todas
        if keyword_lower in n['titulo'].lower() or keyword_lower in n['resumo'].lower()
    ]

    print(f"Filtradas {len(filtradas)} itens com keyword '{keyword}'")
    return filtradas


# ============================================================================
# FUNCAO: Formatar resultado
# ============================================================================

def formatar_noticias(noticias: List[Dict], titulo: str = "NOTICIAS DE IA") -> str:
    """Formata lista de noticias/papers/repos para exibicao."""
    if len(noticias) == 0:
        return "Nenhum item encontrado."

    resultado = f"\n{titulo}\n"
    resultado += "=" * 70 + "\n\n"
    resultado += f"Total: {len(noticias)} itens\n\n"

    # Agrupa por fonte
    fontes_count = {}
    for n in noticias:
        fontes_count[n['fonte']] = fontes_count.get(n['fonte'], 0) + 1

    resultado += "Fontes: " + ", ".join([f"{fonte} ({count})" for fonte, count in fontes_count.items()]) + "\n"
    resultado += "-" * 70 + "\n\n"

    # Lista itens (limita a 50)
    for i, item in enumerate(noticias[:50], 1):
        data_obj = item['data_obj']
        dias_atras = (datetime.now(timezone.utc) - data_obj).days

        if dias_atras == 0:
            quando = "Hoje"
        elif dias_atras == 1:
            quando = "Ontem"
        else:
            quando = f"Ha {dias_atras} dias"

        resultado += f"\n{i}. [{item['fonte']}] {item['titulo']}\n"
        resultado += f"   >>> {item['link']}\n"
        resultado += f"   Data: {data_obj.strftime('%d/%m/%Y')} ({quando})\n"

        # Informacoes adicionais por tipo
        if item['fonte'] == "ArXiv" and 'autores' in item and item['autores']:
            resultado += f"   Autores: {', '.join(item['autores'][:3])}"
            if len(item['autores']) > 3:
                resultado += f" +{len(item['autores']) - 3} mais"
            resultado += "\n"
        elif item['fonte'] == "GitHub" and 'stars' in item:
            resultado += f"   Stars: {item['stars']} | Linguagem: {item.get('linguagem', 'N/A')}\n"

        # Resumo
        resumo = item['resumo']
        if len(resumo) > 250:
            resumo = resumo[:250] + "..."
        if resumo:
            resultado += f"   > {resumo}\n"

    if len(noticias) > 50:
        resultado += f"\n... e mais {len(noticias) - 50} itens\n"

    return resultado


# ============================================================================
# MCP TOOLS
# ============================================================================

@app.list_tools()
async def list_tools() -> list[Tool]:
    """Lista as ferramentas disponiveis."""
    return [
        Tool(
            name="list_ai_news",
            description="Lista TODAS as noticias, papers e repositorios de IA das ultimas 2 semanas. Inclui: 8 blogs (OpenAI, Anthropic, Google AI, DeepMind, Hugging Face, MIT Tech Review, TechCrunch, The Verge) + ArXiv papers + GitHub trending repos. Retorna centenas de itens agregados.",
            inputSchema={
                "type": "object",
                "properties": {
                    "days": {
                        "type": "number",
                        "description": "Numero de dias (padrao: 14)",
                        "default": 14
                    },
                    "include_papers": {
                        "type": "boolean",
                        "description": "Incluir papers do ArXiv (padrao: true)",
                        "default": True
                    },
                    "include_github": {
                        "type": "boolean",
                        "description": "Incluir repositorios GitHub (padrao: true)",
                        "default": True
                    }
                }
            }
        ),
        Tool(
            name="search_ai_content",
            description="Busca noticias, papers ou repos que contenham uma palavra-chave. Busca em titulo e resumo de todas as fontes (blogs, ArXiv, GitHub).",
            inputSchema={
                "type": "object",
                "properties": {
                    "keyword": {
                        "type": "string",
                        "description": "Palavra-chave (ex: 'GPT', 'transformer', 'vision')"
                    },
                    "days": {
                        "type": "number",
                        "description": "Numero de dias (padrao: 14)",
                        "default": 14
                    }
                },
                "required": ["keyword"]
            }
        ),
        Tool(
            name="list_arxiv_papers",
            description="Lista apenas papers academicos recentes do ArXiv em categorias de IA/ML (cs.AI, cs.LG, cs.CL, cs.CV, stat.ML).",
            inputSchema={
                "type": "object",
                "properties": {
                    "days": {
                        "type": "number",
                        "description": "Numero de dias (padrao: 14)",
                        "default": 14
                    },
                    "max_results": {
                        "type": "number",
                        "description": "Maximo de papers (padrao: 50)",
                        "default": 50
                    }
                }
            }
        ),
        Tool(
            name="list_github_trending",
            description="Lista repositorios populares de IA no GitHub (por stars). Filtra por topicos: AI, ML, deep-learning, LLM, transformers, etc.",
            inputSchema={
                "type": "object",
                "properties": {
                    "days": {
                        "type": "number",
                        "description": "Numero de dias (padrao: 14)",
                        "default": 14
                    }
                }
            }
        ),
        Tool(
            name="list_sources",
            description="Lista todas as fontes configuradas (blogs RSS, ArXiv, GitHub) e seus status.",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Executa as tools."""

    if name == "list_ai_news":
        days = arguments.get("days", 14)
        include_papers = arguments.get("include_papers", True)
        include_github = arguments.get("include_github", True)

        noticias = buscar_todas_fontes(dias=days, incluir_papers=include_papers, incluir_github=include_github)
        resultado = formatar_noticias(noticias, f"CONTEUDO DE IA - ULTIMOS {days} DIAS")
        return [TextContent(type="text", text=resultado)]

    elif name == "search_ai_content":
        keyword = arguments.get("keyword", "")
        days = arguments.get("days", 14)

        if not keyword:
            return [TextContent(type="text", text="Erro: keyword nao fornecida")]

        noticias = buscar_por_keyword(keyword, days)
        resultado = formatar_noticias(noticias, f"BUSCA: '{keyword}' ({days} dias)")
        return [TextContent(type="text", text=resultado)]

    elif name == "list_arxiv_papers":
        days = arguments.get("days", 14)
        max_results = arguments.get("max_results", 50)

        papers = buscar_arxiv_papers(dias=days, max_results=max_results)
        resultado = formatar_noticias(papers, f"PAPERS ARXIV ({days} dias)")
        return [TextContent(type="text", text=resultado)]

    elif name == "list_github_trending":
        days = arguments.get("days", 14)

        repos = buscar_github_trending(dias=days)
        resultado = formatar_noticias(repos, f"GITHUB TRENDING AI ({days} dias)")
        return [TextContent(type="text", text=resultado)]

    elif name == "list_sources":
        resultado = "\nFONTES CONFIGURADAS\n"
        resultado += "=" * 70 + "\n\n"

        resultado += "BLOGS RSS:\n"
        for fonte_id, config in FONTES_RSS.items():
            status = "ATIVA" if config['ativa'] else "INATIVA"
            resultado += f"  [{status}] {config['nome']}\n"

        resultado += f"\nARXIV:\n"
        resultado += f"  [ATIVA] ArXiv Papers\n"
        resultado += f"  Categorias: {', '.join(ARXIV_CATEGORIAS)}\n"

        resultado += f"\nGITHUB:\n"
        resultado += f"  [ATIVA] GitHub Trending AI\n"

        total = len(FONTES_RSS) + 2
        resultado += f"\nTotal: {total} fontes ativas\n"

        return [TextContent(type="text", text=resultado)]

    else:
        return [TextContent(type="text", text=f"Tool desconhecida: {name}")]


# ============================================================================
# INICIALIZACAO
# ============================================================================

async def main():
    """Funcao principal."""
    total_fontes = len([f for f in FONTES_RSS.values() if f['ativa']]) + 2  # +ArXiv +GitHub
    print(f"\nServidor pronto com {total_fontes} fontes ativas!")
    print(f"Blogs: {', '.join([c['nome'] for c in FONTES_RSS.values() if c['ativa']])}")
    print("Papers: ArXiv (cs.AI, cs.LG, cs.CL, cs.CV, stat.ML)")
    print("Repositorios: GitHub Trending AI")
    print("\nAguardando requisicoes...\n")

    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
