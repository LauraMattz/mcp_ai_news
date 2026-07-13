# Dockerfile para deploy em qualquer plataforma
FROM python:3.10-slim

WORKDIR /app

# Copiar requirements e instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar codigo da API
COPY api.py .

# Expor porta
EXPOSE 8000

# Comando para iniciar
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
