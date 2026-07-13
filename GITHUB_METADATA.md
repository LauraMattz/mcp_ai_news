# Metadados do GitHub

Instruções para adicionar metadados ao repositório no GitHub.

## 1. Description (Descrição curta)

No GitHub, vá em **Settings** → edite a descrição:

```
Agregador de notícias sobre IA com MCP Server e REST API. 10 fontes: blogs, ArXiv, GitHub. Deploy gratuito no Render.
```

## 2. Website

Adicione a URL da API live:

```
https://mcp-ai-news.onrender.com
```

## 3. Topics (Tags)

Adicione os seguintes topics no GitHub (Settings → Topics):

```
mcp
model-context-protocol
fastapi
ai-news
artificial-intelligence
machine-learning
arxiv
github-api
rss-feed
news-aggregator
python
claude
anthropic
rest-api
openai
tech-news
papers
research
api
ai
```

## 4. About Section

Complete o "About" com:

- ✅ Description: (ver item 1)
- ✅ Website: (ver item 2)
- ✅ Topics: (ver item 3)
- ✅ Releases: Criar v1.0.0 quando estável
- ✅ Packages: Não aplicável
- ✅ Used by: Deixe GitHub preencher automaticamente

## 5. Social Preview

GitHub gera automaticamente uma imagem de preview. Para customizar:

1. Vá em **Settings** → **Social preview**
2. Upload uma imagem 1280x640 (opcional)
3. Ou deixe o preview automático com README

## 6. README Badges

Já adicionados no README:

- MCP Enabled
- FastAPI version
- Python version
- MIT License
- Deploy status
- Active status

## 7. Repository Settings Recomendados

**Settings → General:**
- ✅ Issues: Habilitado
- ✅ Projects: Desabilitado (opcional)
- ✅ Wiki: Desabilitado
- ✅ Discussions: Desabilitado (ou habilitar para comunidade)

**Settings → Security:**
- ✅ Dependabot alerts: Habilitado
- ✅ Security updates: Habilitado

**Settings → Features:**
- ✅ Wikis: Desabilitado (usar apenas README)
- ✅ Issues: Habilitado
- ✅ Sponsorships: Opcional
- ✅ Preserve this repository: Opcional

## 8. .github Folder (Opcional)

Criar arquivos de comunidade:

### `.github/FUNDING.yml` (se tiver sponsorship):
```yaml
github: LauraMattz
```

### `.github/ISSUE_TEMPLATE/bug_report.md`:
```markdown
---
name: Bug Report
about: Relatar um problema
title: '[BUG] '
labels: bug
---

**Descrição do bug**
Uma descrição clara do problema.

**Como reproduzir**
Passos para reproduzir o comportamento:
1. ...
2. ...

**Comportamento esperado**
O que você esperava que acontecesse.

**Screenshots**
Se aplicável, adicione screenshots.

**Ambiente:**
 - OS: [Windows/Mac/Linux]
 - Python: [ex: 3.10]
 - Versão: [ex: 1.0.0]
```

### `.github/ISSUE_TEMPLATE/feature_request.md`:
```markdown
---
name: Feature Request
about: Sugerir uma nova funcionalidade
title: '[FEATURE] '
labels: enhancement
---

**Descrição da feature**
Uma descrição clara da funcionalidade sugerida.

**Motivação**
Por que essa feature seria útil?

**Solução proposta**
Como você imagina que isso funcionaria?
```

### `.github/PULL_REQUEST_TEMPLATE.md`:
```markdown
## Descrição

Descreva as mudanças neste PR.

## Tipo de mudança

- [ ] Bug fix
- [ ] Nova feature
- [ ] Breaking change
- [ ] Documentação

## Checklist

- [ ] Código segue style guide do projeto
- [ ] Testes foram adicionados/atualizados
- [ ] Documentação foi atualizada
- [ ] Commits seguem convenção (Conventional Commits)
```

## 9. GitHub Actions (CI/CD) - Opcional

### `.github/workflows/test.yml`:
```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.10", "3.11", "3.12"]

    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pytest
    - name: Test imports
      run: |
        python -c "import fastapi; print('FastAPI OK')"
        python -c "import feedparser; print('Feedparser OK')"
```

## 10. Releases

Quando estiver pronto para v1.0:

1. **GitHub → Releases → Create new release**
2. **Tag:** v1.0.0
3. **Title:** AI News Aggregator v1.0.0
4. **Description:**
```markdown
## 🎉 Primeiro Release Oficial

### Features
- MCP Server para Claude Code/Desktop
- REST API com FastAPI
- 10 fontes de conteúdo (8 blogs + ArXiv + GitHub)
- Cache em memória (15 min)
- Deploy gratuito no Render
- Documentação completa

### Instalação
```bash
git clone https://github.com/LauraMattz/mcp_ai_news.git
cd mcp_ai_news
pip install -r requirements.txt
```

### Live API
https://mcp-ai-news.onrender.com/docs
```

## 11. Star History Badge (Opcional)

Adicione ao README quando tiver stars:

```markdown
[![Star History](https://api.star-history.com/svg?repos=LauraMattz/mcp_ai_news&type=Date)](https://star-history.com/#LauraMattz/mcp_ai_news&Date)
```

## 12. Stats Badges (Opcional)

Adicione ao README:

```markdown
![GitHub stars](https://img.shields.io/github/stars/LauraMattz/mcp_ai_news)
![GitHub forks](https://img.shields.io/github/forks/LauraMattz/mcp_ai_news)
![GitHub issues](https://img.shields.io/github/issues/LauraMattz/mcp_ai_news)
![GitHub pull requests](https://img.shields.io/github/issues-pr/LauraMattz/mcp_ai_news)
![GitHub last commit](https://img.shields.io/github/last-commit/LauraMattz/mcp_ai_news)
```

---

**Pronto!** Com esses metadados o repositório ficará profissional e fácil de encontrar.
