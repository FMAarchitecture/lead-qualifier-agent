FROM python:3.11-slim

WORKDIR /app

# Copia os requisitos
COPY ../requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código
COPY . .

# Expõe a porta do FastAPI
EXPOSE 8000

# Sobe o servidor FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
