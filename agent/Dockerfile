FROM python:3.11-slim

WORKDIR /app

# Copia os requisitos da raiz
COPY ../requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o código do repositório (inclusive main.py da raiz)
COPY .. .

# Expõe a porta do FastAPI
EXPOSE 8000

# Sobe o servidor FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
