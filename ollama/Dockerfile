FROM ollama/ollama

EXPOSE 11434

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Sobrescreve o entrypoint padrão 
ENTRYPOINT ["/entrypoint.sh"]
