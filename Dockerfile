FROM ollama/ollama

# Baixa o modelo desejado ao buildar
RUN ollama pull llama3

# Expõe a porta padrão da API
EXPOSE 11434

# Inicia o serviço
CMD ["ollama", "serve"]
