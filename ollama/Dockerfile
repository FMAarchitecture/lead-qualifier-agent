FROM ollama/ollama

# Expondo a porta padrão da API
EXPOSE 11434

# Baixa o modelo já no build (substitua por outro se quiser)
RUN ollama pull llama3

# Inicia o serviço Ollama
CMD ["ollama", "serve"]
